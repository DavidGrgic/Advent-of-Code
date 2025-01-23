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
    data = 3014603
    #data = 5

    # Part 1
    if True:
        circle = {i+1: ((i+1) % data) + 1 for i in range(data)}
        current = 1
        while len(circle) > 1:
            skip = circle[current]
            circle[current] = circle[skip]
            del circle[skip]
            current = circle[current]
        print(f"A1: {next(iter(circle))}")

    # Part 2
    circle = [i+1 for i in range(data)]
    current = 0
    while (len_ := len(circle)) > 1:
        if False and (len_ % (data // 100) == 0): print(len_)
        skip = (current + (len_ // 2)) % len_
        del circle[skip]
        current = (current + (0 if skip < current else 1))  % len(circle)
    print(f"A2: {next(iter(circle))}")

if __name__ == '__main__':
    main()
