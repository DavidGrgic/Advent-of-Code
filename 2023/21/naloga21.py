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
_img_map = {0: '.', 1: 'O'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    data = []
    with open('t.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [1 if i == '#' else 0 for i in ln]
            r = ln.find('S')
            if r >= 0:
                start = (c,r)
            data += [da]
    data = np.array(data)

    plus = lambda x, y: (x[0]+y[0], x[1]+y[1])

    # Part 1
    if False:
        pot = np.zeros_like(data)
        pot[start] = 1
        for _ in range(6):
            idx = np.where(pot == 1)
            pot = np.zeros_like(data)
            for i,j in zip(*idx):
                for s in {(1,0), (-1,0), (0,1), (0,-1)}:
                    i_, j_ = plus((i,j), s)
                    if 0 <= i_ < data.shape[0] and 0 <= j_ < data.shape[1] and data[i_, j_] != 1:
                        pot[i_, j_] = 1
      #      _img_print(pot)
        print(f"A1: {pot.sum()}")
        _img_print(pot)

    # Part 2
    ii = data.shape[0]
    jj = data.shape[1]
    rock = {(i, j) for i, j in zip(*np.where(data))}
    sosed = {}
    for i in range(ii):
        for j in range(jj):
            if (i % ii, j % jj) in rock:
                continue
            sos = {}
            for s in {(1,0), (-1,0), (0,1), (0,-1)}:
                i_, j_ = plus((i,j), s)
                over = 1 if i_ != (i_ % ii) or j_ != (j_ % jj) else 0
                i_ %= ii
                j_ %= jj
                if (i_, j_) not in rock:
                    sos |= {(i_, j_): over}
            sosed.update({(i,j): sos})
    pot = {ij: 0 for ij in sosed}
    pot[start] += 1
    for _ in range(6):
        for ij, v in pot.items():
            for ss in sosed[ij]:
                pot[ss] += v
            pot[ij] -= v
        
    print(f"A2: {len(pot)}")

if __name__ == '__main__':
    main()
