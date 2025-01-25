# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
import string
import hashlib
#from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product, groupby
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
    data = 'ngcjuoqr'
    #data = 'abc'

    md5 = lambda x: hashlib.md5(x.encode()).hexdigest()
    find = lambda x, n: [] if (l := len(x)) < n else [(i, x[i]) for i in range(l-n+1) if len(set(x[i:i+n])) == 1]
    def super_md5(x: str):
        for _ in range(2017):
            x = md5(x)
        return x

    def get_hash(fun = md5, nn: int = 64):
        triple = {k: set() for k in set(string.hexdigits.casefold())}
        keys = set()
        n = 0
        while len(keys) < nn or max(keys) > n - 1000:
            key_ = fun(data+str(n))
            if (f3 := find(key_, 3)):
                triple[f3[0][1]].add(n)
            for k in {c for _,c in find(key_, 5)}:
                keys |= {i for i in triple[k] if i < n <= i+1000}
            n += 1
        return sorted(keys)

    # Part 1
    if True:
        p1 = get_hash()
        print(f"A1: {p1[64-1]}")

    # Part 2
    p2 = get_hash(super_md5)
    print(f"A2: {p2[64-1]}")

if __name__ == '__main__':
    main()
