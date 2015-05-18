#!/usr/bin/python
#
# Adapted from one of the packet sniffer examples bundled with impacket

import sys
import time
import string
import colorsys
import random
import math
import pulse
from threading import Thread

import pcapy
from pcapy import findalldevs, open_live
import impacket
from impacket.ImpactDecoder import EthDecoder, LinuxSLLDecoder

import Queue
from holidaysecretapi import HolidaySecretAPI 

DEVICE_COLOURS = {
    '2' : 46,               # yellow
    '3' : 180,              # cyan
    '4' : 270,              # purple
    '5' : 161,              # mint
    '6' : 270,              # purple
    '7' : 297,              # magenta
    '8' : 23,               # orange
    '9' : 111,              # green
    '10' : 0,               # red
    '11' : 27
}

RETURN_SAME = False

SPEED = .5
SIZE = 3
VALUE = .1

WAIT_T = .02


def local_ip_to_rgb(ip):
    ipa = ip.split('.')
    if ipa:
        last = ipa.pop()
        if last in DEVICE_COLOURS:
            return colorsys.hsv_to_rgb(DEVICE_COLOURS[last] / 360.0, 1, VALUE)
    return colorsys.hsv_to_rgb(1, 0, VALUE)

def ip_to_rgb(ip):
     ipa = ip.split('.')
     if len(ipa) > 2:
         r = int(float(ipa[0]) * 0.25)
         g = int(float(ipa[1]) * 0.25)
         b = int(float(ipa[2]) * 0.25)
         return (r, g, b)
     else:
         colorsys.hsv_to_rgb(1, 0, VALUE)


def size_to_length(s):
    hex = "%x" % s
    return len(hex)


def make_pulse(col, l):
    grad = [float(g)/l for g in range(l, 0, -1)]
    (r, g, b) = col
    return [ ( r * gr, g * gr, b * gr ) for gr in grad ]


class DecoderThread(Thread):
    def __init__(self, pcapObj, queue):
        # Query the type of the link and instantiate a decoder accordingly.
        datalink = pcapObj.datalink()
        if pcapy.DLT_EN10MB == datalink:
            self.decoder = EthDecoder()
        elif pcapy.DLT_LINUX_SLL == datalink:
            self.decoder = LinuxSLLDecoder()
        else:
            raise Exception("Datalink type not supported: " % datalink)
        self.queue = queue
        self.pcap = pcapObj
        Thread.__init__(self)

    def run(self):
        # Sniff ad infinitum.
        # PacketHandler shall be invoked by pcap for every packet.
        self.pcap.loop(0, self.packetHandler)

    def packetHandler(self, hdr, data):
        # Use the ImpactDecoder to turn the rawpacket into a hierarchy
        # of ImpactPacket instances, then send it to the Visualiser
        # which drives the Holiday lights.
        try:
            p = self.decoder.decode(data)
        except (Exception, KeyboardInterrupt) as e:
            print e
            return
        try:
            protocol = p.child().__class__.__name__
            size = p.get_size()
            src = False
            if protocol == 'IP' or protocol == 'UDP':
                src = p.child().get_ip_src()
                dest = p.child().get_ip_dst()
            elif protocol == 'IP6':
                src = p.child().get_source_address()
                dest = p.child().get_destination_address()
                print "IP6", src, dest
                src = False
            if src:
                l = size_to_length(size)
                if src[0:2] == '10':
                    col = local_ip_to_rgb(src)
                    #col = ip_to_rgb(dest)
                    v = SPEED / l
                    i = 0
                else:
                    if RETURN_SAME:
                        col = local_ip_to_rgb(src)
                    else:
                        col = ip_to_rgb(src)
                    v = -SPEED / l
                    i = -52
                gradient = make_pulse(col, l)
                #print gradient
                self.queue.put(pulse.Pulse(i, v, gradient))
                #print protocol, src, " -> ", dest, "Size ", size
        except Exception as e:
            print "Decoding failed"
            print e
            return


def getInterface():
    # Grab a list of interfaces that pcap is able to listen on.
    # The current user will be able to listen from all returned interfaces,
    # using open_live to open them.
    ifs = findalldevs()

    # No interfaces available, abort.
    if 0 == len(ifs):
        print "You don't have enough permissions to open any interface on this system."
        sys.exit(1)

    # Only one interface available, use it.
    elif 1 == len(ifs):
        print 'Only one interface present, defaulting to it.'
        return ifs[0]

    # Ask the user to choose an interface from the list.
    count = 0
    for iface in ifs:
        print '%i - %s' % (count, iface)
        count += 1
    idx = int(raw_input('Please select an interface: '))

    return ifs[idx]

def main(ip, filter):
    dev = getInterface()

    # Open interface for catpuring.
    p = open_live(dev, 1500, 0, 100)

    # Set the BPF filter. See tcpdump(3).
    p.setfilter(filter)

    print "Listening on %s: net=%s, mask=%s, linktype=%d" % (dev, p.getnet(), p.getmask(), p.datalink())

    q = Queue.Queue()
    
    # Start the holiday visualiser
    pulses = pulse.Pulser(ip, q, WAIT_T)
    pulses.start()

    # Start sniffing thread and finish main thread.
    dt = DecoderThread(p, q)
    dt.start()
    while True:
        try:
            time.sleep(0.01)
        except KeyboardInterrupt:
            dt.terminate = True
            pulses.terminate = True
            sys.exit(0)



# Process command-line arguments. Take everything as a BPF filter to pass
# onto pcap. Default to the empty filter (match all).

if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
    else:
        print "Usage: sniffy.py HOLIDAY_IP"
        sys.exit(1)                 # If not there, fail

    # filter out all traffic to the lights...

    filter = 'not host ' + addr

    main(addr, filter)
