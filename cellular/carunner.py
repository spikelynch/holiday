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

from cellular import CellularAutomaton, rule30, rule90, rule110, basic_mod
import gradient

SLEEP = .1




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
    gradient = gradient.hsvgrad(20, 1, 0, 1, 1, 0, 0)
    print gradient
    ca = CellularAutomaton(gradient, basic_mod)
    app.setup(ca)
    app.start()
    
    while True:
        try:
            time.sleep(SLEEP)
        except KeyboardInterrupt:
            app.terminate = True
            sys.exit(0)
