#!/usr/bin/python
#
"""
First Holiday app
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'MIT'

import sys, time, threading, random, colorsys
from holidaysecretapi import HolidaySecretAPI 


def toholiday(f):
    return int(63 * f)

def rgbtoholiday(r, g, b):
    return ( toholiday(r), toholiday(g), toholiday(b) )

def lerp(a1, a2, k):
    return a1 + (a2 - a1) * k

# note that the HSV-isation leads to very counterintuitive gradients

def mkgradient(r1, g1, b1, r2, g2, b2, n):
    gradient = []
    ( h1, s1, v1 ) = colorsys.rgb_to_hsv(r1, g1, b1)
    ( h2, s2, v2 ) = colorsys.rgb_to_hsv(r2, g2, b2)
    fn = float(n)
    for i in range(n - 1):
        k = i / fn
        h = lerp(h1, h2, k)
        s = lerp(s1, s2, k)
        v = lerp(v1, v2, k)
        ( r, g, b ) = colorsys.hsv_to_rgb(h, s, v)
        gradient.append(rgbtoholiday(r, g, b))
    return gradient
        
# white to green to white to red to white

g1 = mkgradient(1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 8) 
g2 = mkgradient(0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 8) 
g3 = mkgradient(1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 8) 
g4 = mkgradient(1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 8) 

chrimbo = [ (63, 63, 63), (63, 63, 63), (63, 0, 0), (63, 0, 0), (0, 63, 0), (0, 63, 0) ]

chrimbo_gradient = g1 + g2 + g3 + g4

r2y = mkgradient(1, 0, 0, 1, 1, 0, 50)
y2b = mkgradient(1, 1, 0, 0, 0, 1, 50)
b2r = mkgradient(0, 0, 1, 1, 0, 0, 50)

pattern = chrimbo

#print y2b
#print b2r

class Chaserapp(threading.Thread):

    def run(self):
        """Go"""
        global addr
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=addr)
        self.tick = 0
        self.n = len(pattern)
        while True:
            if self.terminate:
                return
            for i in range(self.holiday.NUM_GLOBES):
                k = (i + self.tick) % self.n
                ( r, g, b ) = pattern[k]
                self.holiday.setglobe(i, r, g, b)
            self.tick += 1
            self.holiday.render()  
            time.sleep(.3)       



if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
        cli = sys.argv[2:]
    else:
        sys.exit(1)                 # If not there, fail

    app = Chaserapp()               # Instance thread & start it
    app.start()
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            app.terminate = True
            sys.exit(0)
