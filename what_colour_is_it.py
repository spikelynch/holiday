#!/usr/bin/python
#
"""
Based on http://whatcolourisit.scn9a.org/
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'MIT'

import sys, time, datetime, threading, random, colorsys
from holidaysecretapi import HolidaySecretAPI 

BOOST_VALUE = 1

def hextocol(h):
    return float(h) / 255

def coltohol(fl):
    return int(63 * fl)

def normalisecol(r, g, b):
    ( h, s, v ) = colorsys.rgb_to_hsv(r, g, b)
    nv = v * BOOST_VALUE
    if nv > 1:
        nv = 1
    return colorsys.hsv_to_rgb(h, s, nv)

def timecolour(tn):
    h = tn.hour
    m = tn.minute
    s = tn.second
    hh = int(str(h), 16)
    hm = int(str(m), 16)
    hs = int(str(s), 16)
    red = hextocol(hh)
    green = hextocol(hm)
    blue = hextocol(hs)
#    ( nr, ng, nb ) = normalisecol(red, green, blue)
    return (coltohol(red), coltohol(green), coltohol(blue))


class Timecolourapp(threading.Thread):

    def run(self):
        """Go"""
        global addr
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=addr)
        self.values = []
        for i in range(self.holiday.NUM_GLOBES):
            self.values.append((0, 0, 0))
        self.render()
        while True:
            if self.terminate:
                return
            nt = datetime.datetime.now()
            col = timecolour(nt)
            self.values.append(col)
            del(self.values[0])
            self.render()       # Send the colours out
            time.sleep(1)       # And finally, wait.

    def render(self):
        for i, (r, g, b) in enumerate(self.values):
            self.holiday.setglobe(i, r, g, b)
        self.holiday.render()


# ZOMFG LET'S DO SOME TESTING
#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
    else:
        sys.exit(1)                 # If not there, fail

    app = Timecolourapp()               # Instance thread & start it
    app.start()
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            app.terminate = True
            sys.exit(0)
