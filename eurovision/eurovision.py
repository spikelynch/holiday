#!/usr/bin/python
#
"""
Eurovision flags
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'MIT'

import sys, time
from holidaysecretapi import HolidaySecretAPI 
import flags


def show_flag(ip, nation):
    if nation in flags.FLAGS:
        holiday = HolidaySecretAPI(addr=ip)
        colours = flags.FLAGS[nation]
        print nation
        for i in range(holiday.NUM_GLOBES):
            ( r, b, g ) = colours[i]
            holiday.setglobe(i, r, g, b)
        holiday.render()
    else:
        print "unknown nation " + nation



if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
    else:
        sys.exit(1)                 # If not there, fail

    if len(sys.argv) > 2:
        nation = sys.argv[2]
    else:
        nation = 'france'

    while True:
        show_flag(addr, nation)
        time.sleep(1)
