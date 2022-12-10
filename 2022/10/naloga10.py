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
            da = ln.split(' ')
            data += [da]

    # Part 1
    reg = [1]
    if True:
        dat=copy.deepcopy(data)
        for i in dat:
            for k, j in enumerate(i):
                reg += [reg[-1]]
                if k == 1:
                    reg[-1] += int(j)
        p1 = [(20+40*i, k) for i, k in enumerate(reg[19:230:40])]
        p1 = sum(math.prod(i) for i in p1)
        print(f"A1: {p1}")

    # Part 2
    scr = np.zeros((6,40)).astype(int) * -1
    for i in range(scr.shape[0]):
        for j in range(scr.shape[1]):
            spr = reg[i*scr.shape[1]+j]
            scr[i,j] = 1 if spr-1 <= j <= spr+1 else 0
    _img_print(scr)

if __name__ == '__main__':
    main()
