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
        for c, ln in enumerate(file):
            da = ln.replace('\n', '').split(' must be finished before step ')
            data.append((da[0].split()[-1], da[1].split()[0]))

    # Part 1
    if True:
        parts_ = len(parts := {j for i in data for j in i})
        order = []
        while (order_ := len(order)) < parts_:
            if order_ == 0:
                candidate = {i for i,_ in data} - {j for _,j in data}
            else:
                candidate = {p for p in parts - set(order) if all(i in order for i,j in data if j == p)}
            order.append(sorted(candidate)[0])
        print(f"A1: {''.join(order)}")

    # Part 2
    bias, workers = (60, 5) if len(data) > 8 else (0, 2)
    parts_ = len(parts := {j: None for i in data for j in i})
    t = 0
    while any(i != 0 for i in parts.values()):
        if t == 0:
            candidate = {i for i,_ in data} - {j for _,j in data}
        else:
            todo = {k for k,v in parts.items() if v is None}
            done = {k for k,v in parts.items() if v == 0}
            candidate = {p for p in todo if all(i in done for i,j in data if j == p)}
        start = sorted(candidate)[:workers - sum(i not in {0, None} for i in parts.values())]
        parts = {k: bias + ord(k) - ord('A') + 1 if k in start and v is None else v for k, v in parts.items()}
        t += 1
        parts = {k: v if v is None else max(v-1, 0) for k, v in parts.items()}
    print(f"A2: {t}")

if __name__ == '__main__':
    main()
