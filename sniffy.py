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
    '2' : 180,
    '3' : 46,
    '4' : 230,
    '5' : 161,
    '6' : 230,
    '7' : 297,
    '8' : 23,
    '9' : 111,
    '10' : 0,
    '11' : 27
}

SPEED = .5
SIZE = 3
VALUE = .4



def ip_to_rgb(ip):
    ipa = ip.split('.')
    if ipa:
        last = ipa.pop()
        if last in DEVICE_COLOURS:
            return colorsys.hsv_to_rgb(DEVICE_COLOURS[last] / 360.0, 1, VALUE)
    return colorsys.hsv_to_rgb(1, 0, VALUE)

def size_to_length(s):
    hex = "%x" % s
    return len(hex)



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
        except Exception, e:
            print "Exception!"
            print e 
            return
        value = {}
        try:
            value['proto'] = p.child().child().protocol
            protocol = value['proto']
            value['size'] = p.get_size()
            value['src'] = p.child().get_ip_src()
            value['dest'] = p.child().get_ip_dst()
            if value['src'][0:2] == '10':
                col = ip_to_rgb(value['src'])
                v = SPEED
                i = 0
            else:
                col = ip_to_rgb(value['dest'])
                v = -SPEED
                i = 52
            l = size_to_length(value['size'])
            self.queue.put(pulse.Pulse(i, v, [ col ] * l))
            print "Packet ", value['src'], " -> ", value['dest'], "Size ", value['size']
        except Exception, e:
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
    pulses = pulse.Pulser(ip, q)
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
