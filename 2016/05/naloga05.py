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
    data = 'wtnhxymk'
    #data = 'abc'

    md5 = lambda x: hashlib.md5(x.encode()).hexdigest()

    # Part 1
    if True:
        p1 = ''
        i = 0
        while True:
            if (h := md5(data+str(i)))[:5] == '00000':
                p1 += h[5]
                if len(p1) >= 8:
                    break
            i += 1
        print(f"A1: {p1}")

    # Part 2
    p2 = [None] * 8
    i = 0
    while True:
        if (h := md5(data+str(i)))[:5] == '00000' and h[5].isnumeric() and 0 <= (p := int(h[5])) <= 7 and p2[p] is None:
            p2[p] = h[6]
            if all(i is not None for i in p2):
                break
        i += 1
    print(f"A2: {''.join(p2)}")

if __name__ == '__main__':
    main()
