# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product
#from functools import cache   # @cache
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
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
    data = set()
    location = {}
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            for j, v in enumerate(ln.replace('\n', '')):
                match v:
                    case '#':
                        pass
                    case '.':
                        data.add((i,j))
                    case _:
                        data.add((i,j))
                        location.update({int(v): (i,j)})

    plus = lambda a, b: tuple(i+j for i,j in zip(a,b))

    edge = [(ij, plus(ij, d)) for ij in data for d in {(1,0), (0,1)} if plus(ij, d) in data]

    # Part 1
    G = nx.Graph()
    G.add_edges_from(edge)
    cycle = {}
    for loc in permutations(set(location)-{0}):
        locat = (0,) + loc
        pot = []
        for i in range(len(locat)-1):
            pot_ = nx.shortest_path(G, location[locat[i]], location[locat[i+1]])
            pot.extend(pot_[bool(i):])
        cycle.update({locat: pot})
    p1 = min(len(i) for i in cycle.values()) - 1
    print(f"A1: {p1}")

    # Part 2
    cycle_return = {}
    for k, v in cycle.items():
        pot_ = nx.shortest_path(G, v[-1], location[0])
        cycle_return.update({k + (0,): v + pot_[1:]})
    p2 = min(len(i) for i in cycle_return.values()) - 1
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
