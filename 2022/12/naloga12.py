# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import math, copy
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
import os, sys
import networkx as nx
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():
    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if 'S' in ln:
                start = (c, ln.index('S'))
            if 'E' in ln:
                end = (c, ln.index('E'))
            ln = ln.replace('S','a').replace('E','z')
            da = [ord(i) for i in ln]
            data += [da]
    data = np.array(data)
    data = (data - data.min()).astype(int)

    plus = lambda x, y: (x[0]+y[0],x[1]+y[1])
    xy = data.shape

    # Part 1
    if True:
        graf = []
        for i in range(xy[0]):
            for j in range(xy[1]):
                for d in [(1,0),(-1,0),(0,1),(0,-1)]:
                    n = plus((i,j),d)
                    if not (0 <= n[0] < xy[0] and 0 <= n[1] < xy[1]):
                        continue
                    if data[n] <= data[(i,j)] + 1:
                        graf += [((i,j), n)]
        G = nx.DiGraph()
        G.add_edges_from(graf)

        p1 = nx.shortest_path(G, start, end)
        print(f"A1: {len(p1)-1}")

    # Part 2
    sta = np.where((data == 0))
    sta = {i for i in zip(sta[0], sta[1])}
    p2 = {}
    for k in sta:
        try:
            p2.update({k: len(nx.shortest_path(G, k, end))})
        except nx.exception.NetworkXNoPath: None
    print(f"A2: {min(p2.values())-1}")

if __name__ == '__main__':
    main()
