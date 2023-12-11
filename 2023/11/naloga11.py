# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product
#from functools import cache   # @cache
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
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
            da = [int(i) for i in ln.replace('.', '0').replace('#','1')]
            data += [da]
    data = np.array(data, dtype = int)



    # Part 1
    def razdalja(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
    
    if True:
        dat=copy.deepcopy(data)
        idx = [i for i, v in enumerate(dat.sum(axis = 0)) for j in ([0] if v > 0 else [0,1])]
        dat = dat[:, idx]
        idx = [i for i, v in enumerate(dat.sum(axis = 1)) for j in ([0] if v > 0 else [0,1])]
        dat = dat[idx, :]
        gal = [(i,j) for i, j in zip(*np.where(dat == 1))]
        pari = combinations(gal, 2)
        razd = [razdalja(i[0], i[1]) for i in combinations(gal, 2)]
        print(f"A1: {sum(razd)}")

    # Part 2
    dat=copy.deepcopy(data)
    old = 10**6
    gal = [(i,j) for i, j in zip(*np.where(dat == 1))]
    idx_x = [(0 if v > 0 else old-1) for v in dat.sum(axis = 1)]
    idx_y = [(0 if v > 0 else old-1) for v in dat.sum(axis = 0)]
    gal = [(i[0] + sum(idx_x[:i[0]]), i[1] + sum(idx_y[:i[1]])) for i in gal]
    pari = combinations(gal, 2)
    razd = [razdalja(i[0], i[1]) for i in combinations(gal, 2)]
    print(f"A2: {sum(razd)}")

if __name__ == '__main__':
    main()
