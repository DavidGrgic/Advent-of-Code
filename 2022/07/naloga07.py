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
            data += [da]

    fs = {}
    dr = ()
#    buf = set()
    for i in data:
        if i[0] == '$':
            if i[1] == 'cd':
                if i[2] == '..':
                    dr = dr[:-1]
                elif i[2] == '/':
                    dr = ()
                else:
                    dr += (i[2],)
            elif i[1] == 'ls':
#                buf = set()
                pass
        else:
            if i[0] == 'dir':
                pass
            else:
                fs.update({dr: fs.get(dr, []) + [(i[1], int(i[0]))]})
#                buf |= {(i[1], int(i[0]))}
#                fs.update({dr: buf})
                

    # Part 1
    if True:
        dat=copy.deepcopy(fs)
        p1 = {}
        kk = {j for i in [[i[:k] for k in range(len(i))] for i in dat.keys()] for j in i}
        #for d in dat.keys():
        for d in kk:
            p1.update({d: sum([sum(i[1] for i in v) for k, v in dat.items() if k[:len(d)] == d])})
        print(f"A1: {sum([v for v in p1.values() if v <= 10**5])}")
        # 1272914

    # Part 2
    dat=copy.deepcopy(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
