#!/usr/bin/python

from random import shuffle

import sys, time, threading, random, colorsys
from holidaysecretapi import HolidaySecretAPI 

COLOURS = [ (1, 0, 0), (0, 1, 0), (0, 0, 1), ( 1, 1, 0 ), ( 1, 0, 1), ( 0, 1, 1 ) ]

# WAIT: the sleep time in seconds between steps.

TEST_LENGTH = 125

WAIT = 0.1

CURSOR = ( 63, 0, 0 )

def rgbtoholiday(r, g, b):
    return ( toholiday(r), toholiday(g), toholiday(b) )

def toholiday(f):
    return int(63 * f)


def lerp(a1, a2, k):
    return a1 + (a2 - a1) * k



class Insertsorter:
    def __init__(self, init, renderer):
        self.list = init
        self.renderer = renderer

    def render(self, cursor):
        self.renderer(self.list, cursor)

    def sort(self):
        for i in range(0, len(self.list)):
            self.insert(i)

    def insert(self, i):
        j = i - 1
        while j > -1:
            if self.list[i] >= self.list[j]:
                break
            j -= 1
        if i != j + 1:
            self.render(i)
            self.list.insert(j + 1, self.list.pop(i))
            self.render(j)
        


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


class Mergesorter:
    def __init__(self, init, renderer):
        self.list = init
        self.renderer = renderer

    def render(self, cursor):
        self.renderer(self.list, cursor)

    def sort(self):
        self.mergesort(0, len(self.list))
        return self.list

    def mergesort(self, start, end):
        if start == end - 1:
            return
        mid = (start + end) / 2
        self.mergesort(start, mid)
        self.mergesort(mid, end)
        self.merge(start, mid, end)
        #self.render(mid)

    def merge(self, start, mid, end):
        self.render(mid)
        left = self.list[start:mid]
        right = self.list[mid:end]
        if not ( left and right ):
            print "Error: empty list(s)", left, right
            exit(0)
        i = start
        while left and right:
            if left[0] <= right[0]:
                self.list[i] = left.pop(0)
            else:
                self.list[i] = right.pop(0)
            i += 1
        while left:
            self.list[i] = left.pop(0)
            i += 1
        while right:
            self.list[i] = right.pop(0)
            i += 1




            


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
        list = range(self.holiday.NUM_GLOBES)
        shuffle(list)
        self.makegradient()
        sorter = self.makesorter(list)
        sorter.sort()
        self.render(list, -1)

    def makesorter(self, list):
        sorterc = random.choice([Insertsorter, Quicksorter, Mergesorter])
        print "Sort algorithm: ", sorterc
        sorter = sorterc(list, lambda l, c: self.render(l, c))
        return sorter

    def render(self, list, cursor):
        i = 0
        for l in list:
            ( r, g, b ) = self.gradient(l)
            self.holiday.setglobe(i, r, g, b)
            i += 1
        if cursor > -1:
            self.holiday.setglobe(cursor, *CURSOR)
        self.holiday.render()
        time.sleep(WAIT)

    def makegradient(self):
        #c = random.sample(COLOURS, 2)
        self.grvalues = []
        h1 = random.random()
        h2 = h1 + .5 + random.uniform(-.25, .25)
        if h2 > 1:
            h2 -= 1
        s1 = random.uniform(.5, 1)
        s2 = random.uniform(.5, 1)
        n = self.holiday.NUM_GLOBES
        fn = float(n)
        
        for i in range(n):
            k = i / fn
            h = lerp(h1, h2, k)
            s = lerp(s1, s2, k)
            ( r, g, b ) = colorsys.hsv_to_rgb(h, s, 1)
            self.grvalues.append(rgbtoholiday(r, g, b))
        
        self.gradient = lambda i: self.grvalues[i]


def printrender(list, cursor):
    out = ""
    for i in range(len(list)):
        if i == cursor:
            out += "[" + str(list[i]) + "] "
        else:
            out += str(list[i]) + " "
    print out


def testsort():
    list = range(TEST_LENGTH)
    shuffle(list)
    sorter = Insertionsorter(list, printrender)
    printrender(list, -1)
    sorter.sort()
    printrender(list, -1)




if __name__ == '__main__':
    if len(sys.argv) > 1:
        addr = sys.argv[1]          # Pass IP address of Holiday on command line
        app = Sorterapp()           # Instance thread & start it
        app.start()
        while True:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                app.terminate = True
                sys.exit(0)
    else:
        testsort()


