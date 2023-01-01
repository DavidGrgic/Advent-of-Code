# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import copy, math, time
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
from joblib import Parallel, delayed, cpu_count
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))


def main():
    # Read
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = [int(i) for i in ln]

    # Part 1
    if True:
        N = len(data)
        pattern = []
        for i in range(N):
            patt = [0] * (i+1) + [1] * (i+1) + [0] * (i+1) + [-1] * (i+1)
            pattern.append((patt * (N // len(patt) + 1))[1:N+1])
        dat = copy.deepcopy(data)
        for _ in range(100):
            _dat = []
            for i in range(N):
                _dat.append(abs(sum(v*p for v, p in zip(dat, pattern[i]))) % 10)
            dat = _dat
        print(f"A1: {''.join(str(i) for i in dat[:8])}")

    # Part 2
    NN = 10000
    pos = int(''.join(str(i) for i in data[:7]))
    dat = (data[(pos % len(data))-len(data):] + (NN - 1 - pos // len(data)) * data)[::-1]
    assert NN* len(data) > 2* len(dat), "Prdpostavimo, da je pattern 0,1,0,-1 vedno v obmocju 0,1"
    for k in range(100):
        _dat = []
        tot = 0
        for i in dat:
            tot = (tot + i) % 10
            _dat.append(tot) 
        dat = _dat
    dat = dat[::-1]
    print(f"A2: {''.join(str(i) for i in dat[:8])}")

if __name__ == '__main__':
    main()
