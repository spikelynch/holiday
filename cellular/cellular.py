import random, gradient


class CellularAutomaton(object):

    SCALE = 50
    
    def __init__(self, gradient, rule):
        self.cells = []
        self.gradient = gradient
        self.domain = range(0, len(gradient))
        self.max = len(gradient)
        self.rule = rule
    
    def start(self, n):
        self.n = n
        for i in range(0, self.n):
            self.cells.append(random.choice(self.domain))
    
    def step(self):
        self.newcells = []
        for i in range(0, self.n):
            self.newcells.append(self.value(i))
        self.cells = self.newcells

    def value(self, i):
        l = self.cells[i - 1]
        if i == self.n - 1:
            r = self.cells[0]
        else:
            r = self.cells[i + 1]
        v = self.rule(l, self.cells[i], r) % self.max
        return v

    def cell(self, i):
        return self.gradient[self.cells[i]]
        
def rule90(a, b, c):
    """ Expects a gradient with domain 0, 1 """
    if (a and not c) or (not a and c):
        return 1
    else:
        return 0


def rule30(a, b, c):
    if (a and b) or (a and c) or (not a and not b and not c):
        return 0
    else:
        return 1

def rule110(a, b, c):
    if ( a and b and c ) or a or ( not a and not b and not c ):
        return 0
    else:
        return 1


def basic_mod(a, b, c):
    return a + b + c


def excitable(a, b, c):
    """0 = refractory, 1 = rest, 2 + = excited"""
    if b > 1:
        return b + 1
    if b == 0:
        return 1
    if b == 1:
        if a > 1 or c > 1:
            return 2
        else:
            return 1

        
