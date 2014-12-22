#!/usr/bin/python
#
"""
Holiday app - blend three sine patterns for R G B
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'MIT'

import sys, time, threading, random, math
from holidaysecretapi import HolidaySecretAPI 


SINELENGTH = 400
RMULT = 2
BMULT = 3
GMULT = 5

RV = 0.522
BV = -.3
GV = .735

RON = 1
GON = 1
BON = 1

SLEEP = 0.01

class Sineapp(threading.Thread):

    def run(self):
        """Run the """
        global addr
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=addr)
        self.init()
        self.tick = 0
        while True:
            if self.terminate:
                return
            roff = int(self.tick * RV)
            goff = int(self.tick * GV)
            boff = int(self.tick * BV)
            for i in range(self.holiday.NUM_GLOBES):
                ri = (roff + RMULT * i * self.atog) % SINELENGTH
                gi = (goff + GMULT * i * self.atog) % SINELENGTH
                bi = (boff + BMULT * i * self.atog) % SINELENGTH
                self.holiday.setglobe(i, self.sine[ri], self.sine[gi], self.sine[bi])
            self.holiday.render()       # Send the colours out
            time.sleep(SLEEP)
            self.tick += 1
        
        

    def init(self):
        """Builds a shape based on a sinewave"""
        self.sine = []
        for i in range(SINELENGTH):
            theta = 2.0 * math.pi * i / SINELENGTH
            self.sine.append(int(32 + 31 * math.sin(theta)))
        self.atog = SINELENGTH / self.holiday.NUM_GLOBES
        
        



if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
    else:
        sys.exit(1)                 # If not there, fail

    app = Sineapp()               # Instance thread & start it
    app.start()
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            app.terminate = True
            sys.exit(0)
