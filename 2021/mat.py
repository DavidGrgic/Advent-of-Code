# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 22:02:08 2020

@author: davidg
"""

def prod(x):
    if hasattr(x, '__iter__'):
        y = x[0]
        if len(x) > 1:
            y *= prod(x[1:])
    else:
        y = x
    return y

def iter2bin(x, reverse = False):
    bi = x if hasattr(x, '__iter__') and not isinstance(x, str) else [x]
    bi = [int(bool(i)) for i in bi][::1 if reverse else -1]
    return sum([b*2**i for i, b in enumerate(bi)])

def iter_abs(x):
    assert hasattr(x, '__iter__') and not isinstance(x, str)
    return tuple(abs(i) for i in x)