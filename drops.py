#!/usr/bin/python
#
"""
Animation
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'MIT'

import sys, time, threading, random, colorsys, math
from holidaysecretapi import HolidaySecretAPI 



def toholiday(f):
    if f > 1:
        return 63
    else:
        return int(63 * f)

def rgbtoholiday(r, g, b):
    return ( toholiday(r), toholiday(g), toholiday(b) )


SIZE = 3
LIMIT = 50
SPEED = 2.3

class Drop:
    def __init__(self):
        self.randomise()

    def randomise(self):
        self.x = random.uniform(0.0, 50.0)
        self.y = random.uniform(-50.0, -10.0)
        h = random.random()
        ( r, g, b ) = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        self.r = r
        self.g = g
        self.b = b

    def show(self):
        print self.x, self.y

    def move(self):
        self.y += SPEED
        if self.y > LIMIT:
            self.randomise()

    def brightness(self, x):
        d = math.hypot(x - self.x, self.y)
        p = 1.0 / (1.0 + d * SIZE)
        return ( p * self.r, p * self.g, p * self.b )


class Dropsapp(threading.Thread):

    def run(self):
        """Go"""
        global addr
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=addr)
        self.n = 8
        self.setup(self.n)
        while True:
            if self.terminate:
                return
            for j in range(self.n):
                self.drops[j].move()
            for i in range(self.holiday.NUM_GLOBES):
                r = 0.0
                b = 0.0
                g = 0.0
                for j in range(self.n):
                    ( r1, g1, b1 ) = self.drops[j].brightness(i)
                    r += r1
                    g += g1
                    b += b1
                self.holiday.setglobe(i, toholiday(r), toholiday(g), toholiday(b))
            self.holiday.render()       # Send the colours out
            time.sleep(.01)       # And finally, wait.


    def setup(self, n):
        """Make some things"""
        self.drops = []
        for i in range(n):
            d = Drop()
            d.show()
            self.drops.append(d)
        

if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
    else:
        sys.exit(1)                 # If not there, fail

    app = Dropsapp()               # Instance thread & start it
    app.start()
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            app.terminate = True
            sys.exit(0)
