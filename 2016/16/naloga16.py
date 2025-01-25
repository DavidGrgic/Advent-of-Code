# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
import hashlib
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
    data = '10111100110001111', 272
    #data = '10000', 20

    dat = [int(i) for i in data[0]]

    def disk(da: list[int], nn: int):
        while len(da) < nn:
            da += [0] + [int(not i) for i in reversed(da)]
        return da[:nn]

    def checksum(da: list[int]):
        while (len_ := len(da)) % 2 == 0:
            da = [len(set(da[i:i+2])) % 2 for i in range(0, len_, 2)]
        return da

    # Part 1
    if True:
        chk = checksum(disk(dat, data[-1]))
        print(f"A1: {''.join(str(i) for i in chk)}")

    # Part 2
    chk = checksum(disk(dat, 35651584))
    print(f"A2: {''.join(str(i) for i in chk)}")

if __name__ == '__main__':
    main()
