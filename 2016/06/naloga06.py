﻿# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from collections import Counter
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
        for l, ln in enumerate(file):
            data.append(ln.replace('\n', ''))

    # Part 1
    word = {}
    if True:
        for dat in data:
            for i, v in enumerate(dat):
                word.update({i: word.get(i, []) + [v]})
        p1 = {k: Counter(w).most_common(1)[0][0] for k, w in word.items()}
        p1 = ''.join(v for _,v in sorted(p1.items()))
        print(f"A1: {p1}")

    # Part 2
    p2 = {k: sorted(Counter(w).items(), key=lambda i: i[1])[0][0] for k, w in word.items()}
    p2 = ''.join(v for _,v in sorted(p2.items()))
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
