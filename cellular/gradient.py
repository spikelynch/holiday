#!/usr/bin/python
#
"""
Utility to make HSV lerp gradients
"""

__author__ = 'Mike Lynch'
__version__ = '1.0'
__license__ = 'MIT'

import random, colorsys


def toholiday(f):
    return int(63 * f)

def holidayrgb(h, s, v):
    ( r0, g0, b0 ) = colorsys.hsv_to_rgb(h, s, v)
    return ( toholiday(r0), toholiday(g0), toholiday(b0) ) 

def lerpl(x1, x2, m):
    """Linear interpolation between x1 and x2 where 0 <= k <= m"""
    return lambda k: x1 + (x2 - x1) * (1.0 * k / m)

def hsvgrad(n, h1, s1, v1, h2, s2, v2):
    """Return an array of n RGB tuples, interpolated between the
    two HSV endpoints"""

    hl = lerpl(h1, h2, n - 1)
    sl = lerpl(s1, s2, n - 1)
    vl = lerpl(v1, v2, n - 1)
    return [ holidayrgb(hl(i), sl(i), vl(i)) for i in range(0, n) ]
    
