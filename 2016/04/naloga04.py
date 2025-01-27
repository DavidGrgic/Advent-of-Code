# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from collections import Counter
from string import ascii_lowercase
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
            da = ln.replace('\n', '').split('-')
            i, c = da[-1][:-1].split('[')
            data.append(('-'.join(da[:-1]), int(i), c))


    # Part 1
    if True:
        p1 = []
        for dat in data:
            if ''.join(i[0] for i in sorted(Counter(dat[0].replace('-','')).items(), key=lambda x: (-x[-1], x[0]))[:5]) == dat[-1]:
                p1.append(dat[1])
        print(f"A1: {sum(p1)}")

    # Part 2
    encrypt_name = lambda x, n: ''.join(' ' if i=='-' else ascii_lowercase[(ascii_lowercase.find(i)+n) % len(ascii_lowercase)] for i in x)
    p2 = []
    for dat in data:
        p2.append((dat[1], encrypt_name(dat[0], dat[1])))
    p2 = [(k, v) for k, v in p2 if v.find('north') >= 0]
    print(f"A2: {p2[0][0]}")

if __name__ == '__main__':
    main()
