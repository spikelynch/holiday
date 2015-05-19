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







if __name__ == '__main__':
    if len(sys.argv) > 2:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
        country = sys.argv[2]
    else:
        sys.exit(1)                 # If not there, fail

    holiday = HolidaySecretAPI(addr=addr)

    if not (country in FLAGS):
        print "Country not found"
        sys.exit(1)
    
    for i in range(holiday.NUM_GLOBES):
        ( r, b, g ) = FLAGS[country][i]
        holiday.setglobe(i, r, g, b)
        print "set globe ", i, r, g, b
        holiday.render()
