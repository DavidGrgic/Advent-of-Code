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