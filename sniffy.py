#!/usr/bin/python
#
# Adapted from one of the packet sniffer examples bundled with impacket

import sys
import time
import string
import colorsys
import random
import math
from threading import Thread

import pcapy
from pcapy import findalldevs, open_live
import impacket
from impacket.ImpactDecoder import EthDecoder, LinuxSLLDecoder

import Queue
from holidaysecretapi import HolidaySecretAPI 



# Boring chaser -  move this to its own module...

class Visqueue(Thread):
    
    def __init__(self, queue):
        self.queue = queue
        Thread.__init__(self)
    
    def run(self):
        """Go"""
        global addr
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=addr)
        self.lights = [ (0, 0, 0) for i in range(self.holiday.NUM_GLOBES) ]
        
        while True:
            if self.terminate:
                return
            # move all the lights
            self.lights.pop(0)
            if not self.queue.empty():
                light = self.queue.get()
            else:
                light = ( 0, 0, 0 )
            self.lights.append(light)
            for i in range(self.holiday.NUM_GLOBES):
                self.holiday.setglobe(i, *self.lights[i])
            self.holiday.render() 
            time.sleep(.01)      



def ip_to_rgb(ip):
    ipa = ip.split('.')
    if len(ipa) > 2:
        r = int(float(ipa[0]) * 0.25)
        g = int(float(ipa[1]) * 0.25)
        b = int(float(ipa[2]) * 0.25)
        return (r, g, b)
    else:
        return (63, 63, 63)



START_Y = -10.0
END_Y = 10.0
SPEED = 0.5
SIZE = 8

# More interesting drops which add together so get brighter as the
# network gets busier

def toholiday(f):
    if f > 1:
        return 63
    else:
        return int(63 * f)



class Drop:
    def __init__(self, col):
        self.x = random.uniform(0.0, 50.0)
        self.y = START_Y
        ( r, g, b ) = col #  colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        self.r = r
        self.g = g
        self.b = b
        self.active = True

    def show(self):
        print self.x, self.y

    def move(self):
        self.y += SPEED
        if self.y > END_Y:
            self.active = False

    def brightness(self, x):
        d = math.hypot(x - self.x, self.y)
        p = 1.0 / (1.0 + d * SIZE)
        return ( p * self.r, p * self.g, p * self.b )


class Dropsapp(Thread):

    def __init__(self, queue):
        self.queue = queue
        Thread.__init__(self)

    def run(self):
        """Go"""
        global addr
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=addr)
        self.n = 8
        self.drops = []
        while True:
            if self.terminate:
                return
            for d in self.drops:
                d.move()            
            self.drops = [d for d in self.drops if d.active]

            for i in range(self.holiday.NUM_GLOBES):
                r = 0.0
                b = 0.0
                g = 0.0
                for d in self.drops:
                    ( r1, g1, b1 ) = d.brightness(i)
                    r += r1
                    g += g1
                    b += b1
                self.holiday.setglobe(i, toholiday(r), toholiday(g), toholiday(b))
            self.holiday.render() 

            if not self.queue.empty():
                p = self.queue.get()
                self.drops.append(Drop(p))

            time.sleep(.01)       












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
            value['size'] = p.get_size
            value['src'] = p.child().get_ip_src()
            value['dest'] = p.child().get_ip_dst()
            if value['src'][0:2] == '10':
                col = ip_to_rgb(value['dest'])
            else:
                col = ip_to_rgb(value['src'])
            self.queue.put(col)
            print "Packet " + value['src'] + " -> " + value['dest']
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

def main(filter):
    dev = getInterface()

    # Open interface for catpuring.
    p = open_live(dev, 1500, 0, 100)

    # Set the BPF filter. See tcpdump(3).
    p.setfilter(filter)

    print "Listening on %s: net=%s, mask=%s, linktype=%d" % (dev, p.getnet(), p.getmask(), p.datalink())

    q = Queue.Queue()
    
    # Start the holiday visualiser
    #viz = Visqueue(q)
    viz = Dropsapp(q)
    viz.start()

    # Start sniffing thread and finish main thread.
    dt = DecoderThread(p, q)
    dt.start()
    while True:
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            dt.terminate = True
            viz.terminate = True
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

    main(filter)
