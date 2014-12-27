#!/usr/bin/python
#
"""
Holiday app - Pascal's Triangle
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'MIT'

import sys, time, threading, random, math, colorsys
from holidaysecretapi import HolidaySecretAPI 

SLEEP = 0.1

ITERS = 100

def toholiday(f):
    return int(63 * f)


def colourwheel(n, s):
    wheel = []
    for i in range(n):
        h = s + float(i) / float(n)
        if h > 1:
            h -= 1
        ( fr, fg, fb ) = colorsys.hsv_to_rgb(h, 1, 1)
        wheel.append(( toholiday(fr), toholiday(fg), toholiday(fb)))
    return wheel
        



class Pascal(threading.Thread):

    def run(self):
        """Run the thang"""
        global addr
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=addr)
        self.reset()
        while True:
            if self.terminate:
                return
            for i in range(self.holiday.NUM_GLOBES):
                col = self.wheel[self.values[i] % self.mod]
                self.holiday.setglobe(i, *col)
                if i == 0:
                    self.values[i] = 1
                else:
                    self.values[i] = self.values[i] + self.values[i - 1]
            self.holiday.render()       # Send the colours out
            time.sleep(SLEEP)
            self.tick += 1
            if self.tick > ITERS:
                self.reset()
            

    def reset(self):
        self.values = [1 for i in range(self.holiday.NUM_GLOBES)]
        self.mod = random.randint(2, 36)
        s = float(self.mod) / 36.0
        self.wheel = colourwheel(self.mod, s)
        self.tick = 0
        print "Pascal mod " + str(self.mod)


        



if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
    else:
        sys.exit(1)                 # If not there, fail

    app = Pascal()               # Instance thread & start it
    app.start()
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            app.terminate = True
            sys.exit(0)
