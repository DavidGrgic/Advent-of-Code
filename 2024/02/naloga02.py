﻿# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#from functools import cache   # @cache
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [int(i) for i in ln.split()]
            data += [da]
    data = [np.array(i) for i in data]

    # Part 1
    if True:
        diff = [np.diff(i) for i in data]
        chk1 = np.array([np.all(i > 0) | np.all(i < 0) for i in diff])
        chk2 = np.array([np.all((1 <= np.abs(i)) & (np.abs(i) <= 3)) for i in diff])
        chk = chk1 & chk2
        print(f"A1: {chk.sum()}")

    # Part 2
    def check(dat):
        diff = np.diff(dat)
        chk1 = np.all(diff > 0) | np.all(diff < 0)
        chk2 = np.all((1 <= np.abs(diff)) & (np.abs(diff) <= 3))
        return bool(chk1 & chk2)
    
    p2 = []
    for da in data:
        if d := check(da):
            p2.append(d)
            continue
        else:
            d = False
            for i in range(len(da)):
                if d := check(np.concatenate((da[:i], da[i+1:]))):
                    break
            p2.append(d)
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()