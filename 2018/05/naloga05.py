﻿# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from string import ascii_lowercase, ascii_uppercase
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
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            data = ln.replace('\n', '')

    react = {i+j for i,j in zip(ascii_lowercase, ascii_uppercase)}
    react |= {i[::-1] for i in react}

    def collapse(dat):
        while True:
            dat_ = copy.copy(dat)
            for i in react:
                dat_ = dat_.replace(i, '')
            if len(dat) == len(dat_):
                return dat
            dat = dat_

    # Part 1
    if True:
        p1 = collapse(copy.copy(data))
        print(f"A1: {len(p1)}")

    # Part 2
    p2 = {}
    for i, j in zip(ascii_lowercase, ascii_uppercase):
        p2.update({i: len(collapse(copy.copy(data).replace(i,'').replace(j,'')))})
    print(f"A2: {min(p2.values())}")

if __name__ == '__main__':
    main()
