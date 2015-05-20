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
        self.state = False
        self.nation = 'australia'
    
    def send(self, nation):
        if nation in flags.FLAGS:
            self.nation = nation

    def tick(self):
        if self.state:
            self._off()
            self.state = False
        else:
            self._on()
            self.state = True

    def _on(self):
        colours = flags.FLAGS[self.nation]
        for i in range(self.holiday.NUM_GLOBES):
            ( r, b, g ) = colours[i]
            self.holiday.setglobe(i, r, g, b)
        self.holiday.render()


    def _off(self):
        for i in range(self.holiday.NUM_GLOBES):
            self.holiday.setglobe(i, 0, 0, 0)
        self.holiday.render()
    

