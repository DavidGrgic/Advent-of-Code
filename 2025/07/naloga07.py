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
    split = set()
    with open('d.txt', 'r') as file:
        for l, ln in enumerate(file):
            ln = ln.replace('\n', '')
            for i, v in enumerate(ln):
                match v:
                    case '.':
                        pass
                    case 'S':
                        start = (l, i)
                    case '^':
                        split.add((l, i))
                    case _:
                        raise ValueError()

    # Part 1
    if True:
        p1 = 0
        beam = [[start]]
        for j in range(l):
            row = set()
            spl = {s[1] for s in split if s[0] == j+1}
            for b in beam[-1]:
                if b[1] in spl:
                    row |= {(j+1, b[1]-1), (j+1, b[1]+1)}
                    p1 += 1
                else:
                    row.add((j+1, b[1]))
            beam += [row]
        print(f"A1: {p1}")

    def add(d, k, v):
        if k in d:
            d[k] += v
        else:
            d[k] = v

    # Part 2
    beam = [{start[1]: 1}] # key is column, value is number of beams
    for j in range(l):
        row = {}
        spl = {s[1] for s in split if s[0] == j+1}
        for b, v in beam[-1].items():
            if b in spl:
                add(row, b-1, v)
                add(row, b+1, v)
            else:
                add(row, b, v)
        beam += [row]
    print(f"A2: {sum(beam[-1].values())}")

if __name__ == '__main__':
    main()
