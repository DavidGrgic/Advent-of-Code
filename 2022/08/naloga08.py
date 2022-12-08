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
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [int(i) for i in ln]
            data += [da]
    data = np.array(data)

    # Part 1
    if True:
        dat=copy.deepcopy(data)
        p1= np.zeros_like(dat).astype(bool)
        for i in range(dat.shape[0]):
            vec = dat[i,:]
            res  = np.zeros_like(vec).astype(bool)
            mmm = -1
            for k in range(len(vec)):
                if vec[k] > mmm:
                    res[k] = True
                    mmm = vec[k]
            p1[i,:] |= res
            vec = dat[i,:][::-1]
            res  = np.zeros_like(vec).astype(bool)
            mmm = -1
            for k in range(len(vec)):
                if vec[k] > mmm:
                    res[k] = True
                    mmm = vec[k]
            p1[i,:] |= res[::-1]
        for i in range(dat.shape[1]):
            vec = dat[:,i]
            res  = np.zeros_like(vec).astype(bool)
            mmm = -1
            for k in range(len(vec)):
                if vec[k] > mmm:
                    res[k] = True
                    mmm = vec[k]
            p1[:,i] |= res
            vec = dat[:,i][::-1]
            res  = np.zeros_like(vec).astype(bool)
            mmm = -1
            for k in range(len(vec)):
                if vec[k] > mmm:
                    res[k] = True
                    mmm = vec[k]
            p1[:,i] |= res[::-1]
        print(f"A1: {p1.sum()}")

    # Part 2
    dat=copy.deepcopy(data)
    p2 = np.zeros_like(dat)
    for i in range(dat.shape[0]):
        for j in range(dat.shape[1]):
            tre = dat[i,j]
            vec = ()
            for k in [dat[:i,j][::-1],  dat[i+1:,j],  dat[i,:j][::-1],  dat[i,j+1:]]:
                pog = list(k >= tre)
                vec += (pog.index(True)+1 if True in pog else len(pog)),
            p2[i,j] = math.prod(vec)
    print(f"A2: {p2.max()}")

if __name__ == '__main__':
    main()
