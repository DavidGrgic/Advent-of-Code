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
        for l, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += [tuple(int(i) for i in ln.split(','))]

    idx = lambda a, b: tuple(sorted([a, b]))
    dis = lambda a, b: ((b[0] - a[0])**2 + (b[1] - a[1])**2 + (b[2] - a[2])**2)

    dist = {(x:=idx(data[i], data[j])): dis(*x)
            for i in range(len(data)) for j in range(i+1, len(data))}
    dist = {j[0]: j[1] for j in sorted(dist.items(), key=lambda x: x[1])}
    

    # Part 1
    if True:
        K = 10 ** (1 if len(data) <= 20 else 3)
        k=0
        circ = [{i} for i in data ]
        for a, b in list(dist):
            i = [a in c for c in circ].index(True)
            j = [b in c for c in circ].index(True)
            if i != j:
                circ[i] |= circ[j]
                del circ[j]
            k += 1
            if k >= K:
                break
        p1 = sorted(len(i) for i in circ)[-3:]
        print(f"A1: {math.prod(p1)}")

    # Part 2
    circ = [{i} for i in data ]
    for a, b in list(dist):
        i = [a in c for c in circ].index(True)
        j = [b in c for c in circ].index(True)
        if i != j:
            circ[i] |= circ[j]
            del circ[j]
        if len(circ) == 1:
            break
    print(f"A2: {a[0] * b[0]}")

if __name__ == '__main__':
    main()
