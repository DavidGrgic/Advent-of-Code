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
            data.append(ln.replace('\n', ''))

    keypad = {divmod(i,3): str(i+1) for i in range(9)}
    move = {'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1)}
    plus = lambda a, b: tuple(i+j for i,j in zip(a,b))

    def code(pad):
        ret = []
        pos = {v:k for k,v in pad.items()}['5']
        for dat in data:
            for d in dat:
                if (pos_ := plus(pos, move[d])) in pad:
                    pos = pos_
            ret.append(pad[pos])
        return ret

    # Part 1
    if True:
        p1 = code(keypad)
        print(f"A1: {''.join(p1)}")

    # Part 2
    keypad = {(0,2):'1',
              (1,1):'2', (1,2):'3', (1,3):'4',
              (2,0):'5', (2,1):'6', (2,2):'7', (2,3):'8', (2,4):'9',
              (3,1):'A', (3,2):'B', (3,3):'C',
              (4,2):'D'}
    p2 = code(keypad)
    print(f"A2: {''.join(p2)}")

if __name__ == '__main__':
    main()
