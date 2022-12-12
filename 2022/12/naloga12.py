# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import math, copy
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():
    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if 'S' in ln:
                start = (c, ln.index('S'))
            if 'E' in ln:
                end = (c, ln.index('E'))
            ln = ln.replace('S','a').replace('E','z')
            da = [ord(i) for i in ln]
            data += [da]
    data = np.array(data)
    data = (data - data.min()).astype(int)

    plus = lambda x, y: (x[0]+y[0],x[1]+y[1])
    xy = data.shape

    global nnn
    nnn = 10**6

    def pot(p):
        global nnn
#        print(p)
        res = set()
        for d in [(1,0),(-1,0),(0,1),(0,-1)]:
#            print(d)
            n = plus(p[-1],d)
            if n in p:
                continue
            if not (0 <= n[0] < xy[0] and 0 <= n[1] < xy[1]):
                continue
            if n == end and data[n] <= data[p[-1]] + 1:
                res = {p + (n,)}
                nnn = len(p)
            if data[n] <= data[p[-1]] + 1:
                if len(p) >= nnn:
                    continue
                ppp = pot(p+(n,))
                res |= ppp
        return res
        

    # Part 1
    if True:
#        dat=copy.deepcopy(data)
        poti = pot((start,))
        poti = [p for p in poti if p[-1] == end]
        print(f"A1: {min([len(p) for p in poti])-1}")

    # Part 2
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
