#!/usr/bin/env python
#
"""
Holiday app - General-purpose 1-d cellular automata
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'MIT'

import sys, time, threading, random, math, colorsys

from holidaysecretapi import HolidaySecretAPI 

from cellular import CellularAutomaton
import cellular
import gradient

SLEEP = .02




class CARunner(threading.Thread):

    def setup(self, ca):
        self.ca = ca
        
    def run(self):
        """Run an CellularAutomaton"""
        global addr
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=addr)
        self.ca.start(self.holiday.NUM_GLOBES)
        while True:
            if self.terminate:
                return
            self.ca.step()
            for i in range(self.holiday.NUM_GLOBES):
                self.holiday.setglobe(i, *self.ca.cell(i))
            self.holiday.render()       
            time.sleep(SLEEP)
            

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

    app = CARunner()
    g = gradient.hsvgrad(80, 0, 1, .5, .25, 1, 1) # gnarly purple/green
    #gradient = gradient.hsvgrad(18, 0, .2, .2, 1, 1, 1)
    #gradient = gradient.hsvgrad(67, .16, 1, 1, 0, 1, 0)
    #g = gradient.hsvgrad(20, 0, 1, 1, .3333, 1, .666)
    #g = g + gradient.hsvgrad(20, .3333, 1, .666, .666, 1, .333)
    #g = g + gradient.hsvgrad(20, .666, 1, .333, 1, 1, 0)
    ca = CellularAutomaton(g, cellular.excitable)
    app.setup(ca)
    app.start()
    
    while True:
        try:
            time.sleep(SLEEP)
        except KeyboardInterrupt:
            app.terminate = True
            sys.exit(0)
