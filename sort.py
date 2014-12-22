#!/usr/bin/python

from random import shuffle

import sys, time, threading, random, colorsys
from holidaysecretapi import HolidaySecretAPI 

COLOURS = [ (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1) ]

class Quicksorter:
    def __init__(self, init, renderer):
        self.list = init
        self.renderer = renderer

    def render(self, cursor):
        self.renderer(self.list, cursor)

    def partition(self, start, end):
        pivot = self.list[end]
        bottom = start - 1 
        top = end        
        done = 0
        while not done:
            self.render(pivot)
            while not done: 
                bottom = bottom + 1
                if bottom == top:   
                    done = 1        
                    break

                if self.list[bottom] > pivot:  
                    self.list[top] = self.list[bottom]
                    break

            while not done:  
                top = top - 1  
            
                if top == bottom:
                    done = 1     
                    break

                if self.list[top] < pivot:
                    self.list[bottom] = self.list[top]
                    break                   

        self.list[top] = pivot
        return top 


    def qsort(self, start, end):
        if start < end:
            split = self.partition(start, end)
            self.qsort(start, split - 1)
            self.qsort(split + 1, end)
        else:
            return

    def sort(self):
        self.qsort(0, len(self.list) - 1)
        return self.list

def printrender(list, cursor):
    out = ""
    for i in range(len(list)):
        if i == cursor:
            out += "[" + str(list[i]) + "] "
        else:
            out += str(list[i]) + " "
    print out


def lerp(a1, a2, k):
    return a1 + (a2 - a1) * k
    

def lerpcolour(c1, c2, i):
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2
    j = i * 0.02
    return ( lerp(r1, r2, j), lerp(g1, g2, j), lerp(b1, b2, j) )




class Sorterapp(threading.Thread):

    def run(self):
        """Go"""
        global addr
        self.terminate = False
        self.holiday = HolidaySecretAPI(addr=addr)
        while True:
            if self.terminate:
                return
            self.runsort()
            time.sleep(1)

    def runsort(self):
        list = range(0, 50)
        shuffle(list)
        self.makelerp()
        sorter = Quicksorter(list, lambda l, c: self.render(l, c))
        sorter.sort()
        self.render(list, -1)

    def render(self, list, cursor):
        i = 0
        for l in list:
            ( r, g, b ) = self.lerp(l)
            self.holiday.setglobe(i, int(r * 63), int(g * 63), int(b * 63))
            i += 1
        if cursor > -1:
            self.holiday.setglobe(cursor, 0, 0, 0)
        self.holiday.render()
        time.sleep(0.2)

    def makelerp(self):
        c = random.sample(COLOURS, 2)
        self.lerp = lambda i: lerpcolour(c[0], c[1], i)




if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
    else:
        sys.exit(1)                 # If not there, fail

    app = Sorterapp()               # Instance thread & start it
    app.start()
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            app.terminate = True
            sys.exit(0)

