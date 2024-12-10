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
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data.update({(c,i): int(v) for i, v in enumerate(ln)})

    plus = lambda x, y: (x[0]+y[0], x[1]+y[1])
    diff = lambda x, y: abs(x[0]-y[0]) + abs(x[1]-y[1])

    link = set()
    for ij, v in data.items():
        for s in {(1,0), (-1,0), (0,1), (0,-1)}:
            ij_ = plus(ij,s)
            if data.get(ij_, -72) - v == 1:
                link |= {(ij, ij_)}
    G = nx.DiGraph()
    G.add_edges_from(link)
    starts = {k for k, v in data.items() if v == 0}
    ends = {k for k, v in data.items() if v == 9}
    pairs = {(s,e) for s in starts for e in ends if diff(s,e) <= 9}

    # Part 1
    if True:
        p1 = sum(nx.has_path(G, se[0], se[1]) for se in pairs)
        print(f"A1: {p1}")

    # Part 2
    p2 = 0
    for se in pairs:
        p2 += len([i for i in nx.all_simple_paths(G, se[0], se[1])])
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
