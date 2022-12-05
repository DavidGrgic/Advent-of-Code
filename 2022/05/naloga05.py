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
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    # Read
    ins = False
    data = {}
    nft = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                ins = True
                continue
            if ins:
                da = ln[5:].replace('from', ',').replace('to', ',').split(',')
                nft += [tuple(int(i) for i in da)]
            else:
                da = {1+k: v for k, v in enumerate(ln[1::4]) if v != ' '}
                if da.get(1,'') == '1':
                    continue
                data = {k: [v]+data.get(k,[]) for k, v in da.items()}


    # Part 1
    dat=copy.deepcopy(data)
    if True:
        for i in nft:
            dat[i[2]] += dat[i[1]][-i[0]::][::-1]
            dat[i[1]] = dat[i[1]][:-i[0]]
        print(f"A1: {''.join([i[1][-1] for i in sorted(dat.items())])}")

    # Part 2
    dat=copy.deepcopy(data)
    if True:
        for i in nft:
            dat[i[2]] += dat[i[1]][-i[0]::]
            dat[i[1]] = dat[i[1]][:-i[0]]
        print(f"A2: {''.join([i[1][-1] for i in sorted(dat.items())])}")

if __name__ == '__main__':
    main()
