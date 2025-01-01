﻿# -*- coding: utf-8 -*-
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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            data.extend(ln.replace('\n', '').split(','))


    #        \ n (-1,1) /
    #   nw    +--------+   ne
    # (-1,0) /          \ (0,1)
    # ------+    (0,0)   +-----
    #        \          /
    #   sw    +--------+   se
    # (0,-1) / s (1,-1) \ (1,0)
    move = {'n': (-1,1), 'ne': (0,1), 'se': (1,0), 's': (1,-1), 'sw': (0,-1), 'nw': (-1,0)}
    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])

    start = (0,0)
    track = [start]
    for d in data:
        track.append(plus(track[-1], move[d]))
    end = track[-1]

    # Part 1
    polje = {(i,j) for i in range(min(start[0], end[0]), max(start[0], end[0])+1) for j in range(min(start[1], end[1]), max(start[1], end[1])+1)}
    link = {(ij, plus(ij,m)) for ij in polje for m in {m for k, m in move.items() if k in {'n', 'ne', 'se'}} if plus(ij,m) in polje}
    G = nx.Graph()
    G.add_edges_from(list(link))
    p1 = nx.shortest_path(G, start, end)
    print(f"A1: {len(p1)-1}")

    # Part 2
    # Shortest path, even in honey corrdinates, is actually just sum of both axis.
    p2 = [sum(i) for i in track]
    print(f"A2: {max(p2)}")

if __name__ == '__main__':
    main()
