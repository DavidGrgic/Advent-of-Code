# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys, collections
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    m = 137683
    M = 596253


    # Part 1
    if True:
        valid = []
        x = m
        while x <= M:
            _x = [i for i in str(x)]
            if any(_x[i] == _x[i+1] for i in range(5)) and all(_x[i] <= _x[i+1] for i in range(5)):
                valid.append(x)
            x += 1
        print(f"A1: {len(valid)}")
          
    
    # Part 2
    val = []
    for y in valid:
        _y = [i for i in str(y)]
        if 2 in collections.Counter(_y).values():
            val.append(y)
    print(f"A2: {len(val)}")


if __name__ == '__main__':
    main()
