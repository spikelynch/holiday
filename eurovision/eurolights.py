#!/usr/bin/python
#
"""
Eurovision flags
"""


import sys, time
import flags
from lights import Lights

class EuroLights(Lights):

    def __init__(self, ip):
        Lights.__init__(self, ip)
        self.offset = 0
        self.nation = 'australia'
        self.colours = flags.FLAGS[self.nation]
    
    def send(self, nation):
        if nation in flags.FLAGS:
            self.nation = nation
            self.colours = flags.FLAGS[self.nation]

    def tick(self):
        for i in range(self.holiday.NUM_GLOBES):
            j = (i + self.offset) % self.holiday.NUM_GLOBES
            self.holiday.setglobe(i, *(self.colours[j]))
        self.holiday.render()
        self.offset += 1

    def _off(self):
        for i in range(self.holiday.NUM_GLOBES):
            self.holiday.setglobe(i, 0, 0, 0)
        self.holiday.render()
    

