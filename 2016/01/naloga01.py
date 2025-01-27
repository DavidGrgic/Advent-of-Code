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
            data.extend((d[0], int(d[1:])) for d in ln.replace('\n', '').split(', '))

    plus = lambda a, b: tuple(i+j for i,j in zip(a,b))
    turn = lambda d, t: {(-1,0): (0,-1 if t=='L' else 1),
                         (0,-1): (1 if t=='L' else -1,0),
                         (1,0): (0,1 if t=='L' else -1),
                         (0,1): (-1 if t=='L' else 1,0)}[d]
    distance = lambda a, b=(0,0): sum(abs(i-j) for i,j in zip(a,b))

    # Part 1
    if True:
        position = (0,0)
        direction = (-1,0)
        for trn, mov in data:
            direction = turn(direction, trn)
            for _ in range(mov):
                position = plus(position, direction)
        print(f"A1: {distance(position)}")

    # Part 2
    twice = None
    position = [(0,0)]
    direction = (-1,0)
    for trn, mov in data:
        direction = turn(direction, trn)
        for _ in range(mov):
            position_ = plus(position[-1], direction)
            if position_ in position:
                twice = position_
                break
            else:
                position.append(position_)
        if twice:
            break
    print(f"A2: {distance(twice)}")

if __name__ == '__main__':
    main()
