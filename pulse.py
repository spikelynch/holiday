#!/usr/bin/python

"""
A pulse visualiser 
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'GPL'

import sys, time, random, colorsys, math
from threading import Thread
from Queue import Queue
from holidaysecretapi import HolidaySecretAPI 

HOLIDAY_LENGTH = 50

class Pulse:
    """
    Represents a single pulse with the following attributes:

    velocity (positive or negative)
    gradient (a list of RGB values defining the color and length)
    position (int defining where the pulse is)
    active (Boolean - set to False when the pulse leaves the lights)
    """

    def __init__(self, p, v, g):
        self.position = p
        self.velocity = v
        self.gradient = g
        self.length = len(self.gradient)
        self.active = True

    def move(self):
        """Move this pulse by velocity and deactivate it if it's out"""
        self.position += self.velocity
        if self.velocity < 0:
            if self.position + self.length < 0:
                self.active = False
        else:
            if self.position - self.length > HOLIDAY_LENGTH:
                self.active = False

    def colours(self, i):
        """Return a tuple of this pulse's contribution to light i"""
        if self.velocity < 0:
            return ( 0, 0, 0 )
        gi = [ g for g in range(self.length) if 0 < self.position - g - i < 2 ]
        r1 = 0.0
        b1 = 0.0
        g1 = 0.0
        for g in gi:
            p = self.position - g - i
            ( r0, g0, b0 ) = self.gradient[g]
            if p > 1:
                p = 2 - p
            r1 += r0 * p
            g1 += g0 * p
            b1 += b0 * p
        return (r1, g1, b1)

def toholiday(f):
    if f > 1:
        return 63
    else:
        return int(63 * f)




class Pulser(Thread):
    """
    A Thread which reads a Queue for things to turn into Pulses and
    renders them via the Holiday API.

    p = Pulser(holiday_ip, queue)
    p.run()

    """
    def __init__(self, ip, queue):
        self.queue = queue
        self.ip = ip
        Thread.__init__(self)


    def run(self):
        """Run the thing"""
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=self.ip)
        self.pulses = []
        while True:
            if self.terminate:
                return
            for p in self.pulses:
                p.move()            
            self.pulses = [p for p in self.pulses if p.active]

            for i in range(self.holiday.NUM_GLOBES):
                r = 0
                b = 0
                g = 0
                for p in self.pulses:
                    ( r1, g1, b1 ) = p.colours(i)
                    r += r1
                    g += g1
                    b += b1
                self.holiday.setglobe(i, toholiday(r), toholiday(g), toholiday(b))
            self.holiday.render() 

            if not self.queue.empty():
                p = self.queue.get()
                self.pulses.append(p)

            time.sleep(.05)       


def randcolour(v):
    h = random.uniform(0, 1)
    return colorsys.hsv_to_rgb(h, 1, v)



if __name__ == '__main__':
    if len(sys.argv) > 1:
        ip = sys.argv[1] 
    else:
        print "Usage: pulse.py HOLIDAY_IP"
        sys.exit(1)                 # If not there, fail

    q = Queue()
    
    pulser = Pulser(ip, q)
    pulser.start()

    while True:
        try:
            time.sleep(1)
            if len(pulser.pulses) < 3:
                c = randcolour(1)
                l = random.randint(3, 6)
                v = random.uniform(.01, .5)
                i = 0
                p = Pulse(i, v, [ c ] * l)
                q.put(p)
        except KeyboardInterrupt:
            pulser.terminate = True
            sys.exit(0)

