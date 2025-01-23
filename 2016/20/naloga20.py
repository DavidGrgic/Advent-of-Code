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
def plot(data, mapper: dict = {0: '.', 1: '#'}, default: dict = {set: 1, dict: 0}):
    if isinstance(data, set):
        data = {k: default[set] for k in data}
    if isinstance(data, dict):
        offset = tuple(int(min(i[j] for i in data.keys())) for j in range(2))
        img = np.zeros(tuple(int(max(i[j] for i in data.keys())-offset[j])+1 for j in range(2))).astype(int) + default[dict]
        img[tuple(tuple(int(i[j]-offset[j]) for i in data.keys()) for j in range(2))] = list(data.values())
        data = img
    print('\n'+'\n'.join([''.join(mapper.get(i,'?') for i in j) for j in data]))

def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            data.append(tuple(int(i) for i in ln.replace('\n', '').split('-')))

    # Part 1
    if True:
        rng = [[0, 2**32-1 if len(data) > 5 else 9]]
        for d_m, d_M in data:
            im = max(i for i,(m,M) in enumerate(rng) if m <= d_m)
            iM = min(i for i,(m,M) in enumerate(rng) if M >= d_M)
            if im == iM:
                rng.insert(iM+1, [d_M+1, rng[iM][1]])
                rng[iM][1] = d_m - 1
            else:
                rng[im][1] = min(rng[im][1], d_m - 1)
                rng[iM][0] = max(rng[iM][0], d_M + 1)
                for i in range(iM-1,im,-1):
                    del rng[i]
            rng = [[i,j] for i,j in rng if i<=j]
        print(f"A1: {rng[0][0]}")

    # Part 2
    print(f"A2: {sum(j+1-i for i,j in rng)}")

if __name__ == '__main__':
    main()
