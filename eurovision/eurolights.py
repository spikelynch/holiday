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
        self.send('australia')
    
    def send(self, nation):
        if nation in flags.FRAMES:
            self.nation = nation
            self.frames = flags.FRAMES[self.nation]
            self.f = 0
            self.cycle = False
            return True
        elif nation == 'cycle':
            self.nation = None
            self.cycle = True
        else:
            return False
            
    def tick(self):
        for i in range(self.holiday.NUM_GLOBES):
            self.holiday.setglobe(i, *(self.frames[self.f][i]))
        self.holiday.render()
        self.f += 1
        if self.f == len(self.frames):
            self.f = 0

    def off(self):
        for i in range(self.holiday.NUM_GLOBES):
            self.holiday.setglobe(i, 0, 0, 0)
        self.holiday.render()
    

