#!/usr/bin/python
#
"""
Eurovision flags
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'MIT'

import sys, time, threading
from holidaysecretapi import HolidaySecretAPI 
import flags



class Euroapp(threading.Thread):

    def run(self):
        """Go"""
        global addr
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=addr)
        self.tick = 0
        nations = flags.FLAGS.keys()
        nations.sort()
        while True:
            if self.terminate:
                return
            nation = nations[self.tick]
            colours = flags.FLAGS[nation]
            print nation
            for i in range(self.holiday.NUM_GLOBES):
                ( r, b, g ) = colours[i]
                self.holiday.setglobe(i, r, g, b)
            self.tick += 1
            if self.tick == len(nations):
                self.tick = 0
            self.holiday.render()  
            time.sleep(delay)       





if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
    else:
        sys.exit(1)                 # If not there, fail

    delay = 1
    if len(sys.argv) > 2:
        try:
            delay = float(sys.argv[2])
        except ValueError:
            print "Delay must be numeric"
            sys.exit(1)
            
    holiday = HolidaySecretAPI(addr=addr)

    app = Euroapp()               # Instance thread & start it
    app.start()
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            app.terminate = True
            sys.exit(0)
