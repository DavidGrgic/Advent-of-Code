# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import math
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ({i for i in ln[:int(len(ln)/2)]}, {i for i in ln[int(len(ln)/2):]})
            data += [da]

    pri = lambda x: ord(x)-ord('a') + 1 if ord(x) >= ord('a') else ord(x)-ord('A') + 27
    # Part 1
    if True:
        cist = []
        ddup = []
        for k in data:
            dup = k[0].intersection(k[1])
            cist += [k[0] | k[1]]
            ddup += next(iter(dup))
        print(f"A1: {sum(pri(i) for i in ddup)}")
          
    
    # Part 2
    comm = []
    for k in range(0,len(cist),3):
        cis = cist[k:k+3]
        com = cis[0].intersection(cis[1]).intersection(cis[2])
        comm += [next(iter(com))] 
    print(f"A2: {sum(pri(i) for i in comm)}")


if __name__ == '__main__':
    main()
