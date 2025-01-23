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
def plot(data, mapper: dict = {0: '.', 1: '^'}, default: dict = {set: 1, dict: 0}):
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
    data = {}
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            data.update({(i, j): 1 if v == '^' else 0 for j, v in enumerate(ln.replace('\n', ''))})
    cols = len(data)
    rows = {5: 3, 10: 10}.get(len(data), 40)

    trap = {(1,1,0), (0,1,1), (1,0,0), (0,0,1)}

    def build(data, rows):
        data = data.copy()
        for i in range(1, rows):
            data.update({(i,j): 1 if tuple(data.get((i-1, j+j_), 0) for j_ in range(-1,2)) in trap else 0 for j in range(cols)})
        return data

    # Part 1
    if True:
        dat = build(data, rows)
        #plot(dat)
        print(f"A1: {sum(i==0 for i in dat.values())}")

    # Part 2
    dat = build(data, 400000)
    print(f"A2: {sum(i==0 for i in dat.values())}")

if __name__ == '__main__':
    main()
