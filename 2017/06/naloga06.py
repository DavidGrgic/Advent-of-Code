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
            data = [int(i) for i in ln.split()]

    # Part 1
    if True:
        dat=np.array([data])
        no = dat.shape[1]
        while True:
            da = dat[-1]
            mm = da.max()
            pos = np.asarray(da == mm).nonzero()[0][0]
            val = da[pos]
            da_ = da + (val // no)
            da_[pos] -= val
            for i in range(val % no):
                da_[(pos+i+1) % no] += 1
            dat = np.append(dat, da_.reshape(1,-1), axis=0)
            if (dat[:-1] == da_).all(axis=1).any():
                break
        print(f"A1: {dat.shape[0] - 1}")

    # Part 2
    first = np.asarray((dat[:-1] == da_).all(axis=1)).nonzero()[0][0]
    print(f"A2: {dat.shape[0] - first - 1}")

if __name__ == '__main__':
    main()
