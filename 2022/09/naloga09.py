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
    with open('tdata.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' ')
            data += [(da[0], int(da[1]))]

    mov = {'R': (0,1), 'U': (1,0), 'D': (-1,0), 'L': (0,-1)}

    # Part 1
    hed = [0,0]
    tal = [0,0]
    his = {tuple(tal)}
    if True:
        dat=copy.deepcopy(data)
        for i in dat:
            for j in range(i[1]):

                hed[0] += mov[i[0]][0]
                hed[1] += mov[i[0]][1] 
                diag = (hed[0] != tal[0]) and (hed[1] != tal[1])
                while abs(hed[1]-tal[1]) + abs(hed[0]-tal[0]) > 2 - int(not diag):
                    if hed[1] != tal[1] and hed[0] != tal[0] and diag:
                        tal[0] += np.sign(hed[0] - tal[0])
                        tal[1] += np.sign(hed[1] - tal[1])
                    else:
                        for k in range(2):
                            if abs(hed[k] - tal[k]) > 1:
                                tal[k] += np.sign(hed[k] - tal[k])
                his |= {tuple(tal)}
        print(f"A1: {len(his)}")

    # Part 2
    dat=copy.deepcopy(data)
    rope = [[0,0]] * 10
    his = {tuple(tal)}
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
