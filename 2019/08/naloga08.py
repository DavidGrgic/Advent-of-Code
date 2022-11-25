# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
from collections import Counter
from itertools import permutations, combinations, product
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            data = ln.replace('\n', '')

    #size = (3,2)
    size = (25,6)
    # Part 1
    if True:
        s = mat.prod(size)
        p1 = {}
        assert len(data) % s == 0
        for l in range(len(data) // s):
            sub = data[l*s:(l+1)*s]
            p1.update({l: [[int(i) for i in sub[r*size[0]:(r+1)*size[0]]] for r in range(size[1])]})
        p1_0 = {k: sum(j==0 for i in v for j in i) for k, v in p1.items()}
        p1_0 = [k for k, v in sorted(p1_0.items(), key = lambda x: x[1])]
        p1_l = p1[p1_0[0]]
        p1_res = sum(j == 1 for i in p1_l for j in i) * sum(j == 2 for i in p1_l for j in i)
        print(f"A1: {p1_res}")
          
    
    # Part 2
    img = np.zeros(size) * np.NaN
    for i, r in enumerate(img):
        for j, _ in enumerate(r):
            for k, v in p1.items():
                if v[j][i] == 0:
                    img[i,j] = 0
                    break
                if v[j][i] == 1:
                    img[i,j] = 1
                    break
    print('\n'.join([''.join('#' if i == 1 else ' ' for i in r) for r in img.astype(int).T]))


if __name__ == '__main__':
    main()
