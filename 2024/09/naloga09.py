# -*- coding: utf-8 -*-
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
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = [int(i) for i in ln]

    # Part 1
    if True:
        dat = [(i//2 if (i % 2) == 0 else None) for i, d in enumerate(data) for j in range(d)]
        for i in range(len(dat)-1,-1,-1):
            j = dat.index(None)
            if j > i:
                break
            dat[j], dat[i] = dat[i], dat[j]
        print(f"A1: {sum(i*v for i, v in enumerate(dat) if v is not None)}")

    # Part 2
    indexes = lambda a, b: [(i, i+len(b)) for i in range(len(a)-len(b)+1) if a[i:i+len(b)] == b]
    dat = [(i//2 if (i % 2) == 0 else None) for i, d in enumerate(data) for j in range(d)]
    fixed = set()
    while True:
        val = set(dat) - fixed - {None}
        if len(val) <= 0:
            break
        val = max(val)
        fixed |= {val}
        i, ii = dat.index(val), len(dat) - dat[::-1].index(val)
        j = indexes(dat, [None] * (ii-i))
        if len(j) > 0 and j[0][0] < i:
            dat[j[0][0]:j[0][1]], dat[i:ii] = dat[i:ii], dat[j[0][0]:j[0][1]]
        else:
            continue
    print(f"A2: {sum(i*v for i, v in enumerate(dat) if v is not None)}")

if __name__ == '__main__':
    main()
