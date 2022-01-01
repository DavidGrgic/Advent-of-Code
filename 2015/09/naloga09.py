# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import itertools

def main():

    # Read
    data = {}
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' = ')
            d = da[0].split(' to ')
            data.update({(d[0], d[1]): int(da[1])})
    cities = {i for k in data for i in k}

    # Part 1
    if True:
        paths = itertools.permutations(cities)
        res1 = {}
        for pth in paths:
            res1.update({pth: sum((lambda P = pth, D = data: tuple(D.get((P[i], P[i+1]), D.get((P[i+1], P[i]))) for i in range(len(P)-1)))())})
        print(f"A1: {min(res1.values())}")
          
    
    # Part 2

    print(f"A2: {max(res1.values())}")


if __name__ == '__main__':
    main()
