# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#from functools import cache   # @cache
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
def plot(data, mapper: dict = {0: '#', 1: '.'}, default: dict = {set: 1, dict: 0}):
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
    data = 1362
    #data = 10

    threshold = 30

    plus = lambda a, b: tuple(i+j for i,j in zip(a,b))
    space = lambda a: not (Counter(bin(a[0]**2 + 3*a[0] + 2*a[0]*a[1] + a[1] + a[1]**2 + data)[2:])['1'] % 2)

    # Part 1
    if True:
        start = (1,1)
        end = (31,39) if data != 10 else (7,4)
        node = {(x,y) for x in range(end[0] + threshold) for y in range(end[1] + threshold) if space((x,y))}
        #plot({i[::-1] for i in node})
        edge = [(xy, xy_) for xy in node for d in {(1,0), (0,1)} if (xy_ := plus(xy, d)) in node]
        G = nx.Graph()
        G.add_edges_from(edge)
        path = nx.shortest_path(G, start, end)
        print(f"A1: {len(path) - 1}")

    # Part 2
    p2 = {}
    for pos in node:
        if pos in G and nx.has_path(G, start, pos):
            p2.update({pos: len(nx.shortest_path(G, start, pos))-1})
    print(f"A2: {sum(i <= 50 for i in p2.values())}")

if __name__ == '__main__':
    main()
