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
    data = set()
    with open('d.txt', 'r') as file:
        for l, ln in enumerate(file):
            ln = ln.replace('\n', '')
            for i, v in enumerate(ln):
                if v == '@':
                    data.add((l, i))
                    
    smer = {(i,j) for i in range(-1,2) for j in range(-1,2)} - {(0, 0)}
    plus = lambda x, y: (x[0]+y[0], x[1]+y[1])

    # Part 1
    if True:
        p1 = 0
        dat=copy.deepcopy(data)
        for ij in dat:
            sosedov = sum(plus(ij, s) in dat for s in smer)
            if sosedov < 4:
                p1+=1
        print(f"A1: {p1}")

    # Part 2
    dat=copy.deepcopy(data)
    while True:
        dat_new = set()
        for ij in dat:
            sosedov = sum(plus(ij, s) in dat for s in smer)
            if not sosedov < 4:
                dat_new.add(ij)
        if len(dat) == len(dat_new):
            break
        else:
            dat = dat_new
    print(f"A2: {len(data) - len(dat)}")

if __name__ == '__main__':
    main()
