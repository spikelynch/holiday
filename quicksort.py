#!/usr/bin/python

from random import shuffle

import sys, time, threading, random, colorsys
from holidaysecretapi import HolidaySecretAPI 

COLOURS = [ (1, 0, 0), (0, 1, 0), (0, 0, 1), ( 1, 1, 0 ), ( 1, 0, 1), ( 0, 1, 1 ) ]

# WAIT: the sleep time in seconds between steps.

WAIT = 0.1

def rgbtoholiday(r, g, b):
    return ( toholiday(r), toholiday(g), toholiday(b) )

def toholiday(f):
    return int(63 * f)


def lerp(a1, a2, k):
    return a1 + (a2 - a1) * k

 


# note that the HSV-isation leads to very counterintuitive gradients

def mkgradient(c1, c2, n):
    gradient = []
    ( h1, s1, v1 ) = colorsys.rgb_to_hsv(*c1)
    ( h2, s2, v2 ) = colorsys.rgb_to_hsv(*c2)
    fn = float(n)
    for i in range(n):
        k = i / fn
        h = lerp(h1, h2, k)
        s = lerp(s1, s2, k)
        v = lerp(v1, v2, k)
        ( r, g, b ) = colorsys.hsv_to_rgb(h, s, v)
        gradient.append(rgbtoholiday(r, g, b))
    return gradient











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
        self.makegradient()
        sorter = Quicksorter(list, lambda l, c: self.render(l, c))
        sorter.sort()
        self.render(list, -1)

    def render(self, list, cursor):
        i = 0
        for l in list:
            ( r, g, b ) = self.gradient(l)
            self.holiday.setglobe(i, r, g, b)
            i += 1
        if cursor > -1:
            self.holiday.setglobe(cursor, 0, 0, 0)
        self.holiday.render()
        time.sleep(WAIT)

    def makegradient(self):
        c = random.sample(COLOURS, 2)
        self.grvalues = mkgradient(c[0], c[1], 50)
        self.gradient = lambda i: self.grvalues[i]



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

