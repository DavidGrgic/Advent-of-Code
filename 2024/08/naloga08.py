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
        for i, ln in enumerate(file):
            ln = ln.replace('\n', '')
            for j, v in enumerate(ln):
                if v != '.':
                    data.append((v, (i,j)))
    dim_i = i
    dim_j = j
    dim_m = max(dim_i, dim_j)
    freq = {k: {ij for k_, ij in data if k == k_} for k,_ in data}
    plus = lambda x, y: (x[0]+y[0],x[1]+y[1])

    def node(l1, l2, mul):
        ret = set()
        dif = (l2[0]-l1[0], l2[1]-l1[1])
        for m in mul:
            xy = plus(l1, (m*dif[0], m*dif[1]))
            if 0 <= xy[0] <= dim_i and 0 <= xy[1] <= dim_j:
                ret |= {xy}
        return ret

    def nodes(mul):
        ret = set()
        for k, val in freq.items():
            for l1, l2 in combinations(val, 2):
                ret |= node(l1, l2, mul)
        return ret

    # Part 1
    if True:
        p1 = nodes({-1, 2})
        print(f"A1: {len(p1)}")

    # Part 2
    p2 = nodes(range(-dim_m, 1+dim_m))
    print(f"A2: {len(p2)}")

if __name__ == '__main__':
    main()
