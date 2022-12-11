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
    data = {}; dat = ()
    items = []
    k = 0; d=0
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                data.update({k: dat})
                k += 1
                d = 0
                continue
            da = ln.split(':')
            if d == 1:
                items += [[int(i) for i in da[-1].split(',')]]
            elif d == 2:
                dat = da[-1].split('=')[-1]
            elif d == 3:
                dat = (dat, int(da[-1].split(' ')[-1]))
            elif d == 4:
                dat += (int(da[-1].split(' ')[-1]),)
            elif d == 5:
                dat += (int(da[-1].split(' ')[-1]),)
            d +=1
        data.update({k: dat})

    # Part 1
    ite = copy.deepcopy(items)
    if True:
        p1 = {}
        for r in range(20):
            for k, v in data.items():
                for old in ite[k]:
                    p1.update({k: p1.get(k, 0)+1})
                    new = int(eval(v[0]) / 3)
                    if new % v[1] == 0:
                        ite[v[2]] += [new]
                    else:
                        ite[v[3]] += [new]
                ite[k] = []
        print(f"A1: {math.prod(sorted(p1.values())[-2:])}")

    # Part 2
    ite = copy.deepcopy(items)
    lcm = math.lcm(*(i[1] for i in data.values()))
    p2 = {}
    for r in range(10000):
        for k, v in data.items():
            for old in ite[k]:
                p2.update({k: p2.get(k, 0)+1})
                new = int(eval(v[0])) % lcm
                if new % v[1] == 0:
                    ite[v[2]] += [new]
                else:
                    ite[v[3]] += [new]
            ite[k] = []
    print(f"A2: {math.prod(sorted(p2.values())[-2:])}")

if __name__ == '__main__':
    main()
