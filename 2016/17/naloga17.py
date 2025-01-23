# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
import hashlib
from collections import Counter
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
    data = 'qljzarfv'
    #data = 'ulqzkmiv'
    #data = 'kglvqrro'
    #data = 'ihgpwlah'
    #data = 'hijkl'

    direction = {(1,0): 'D', (-1,0): 'U', (0,1): 'R', (0,-1): 'L'}
    plus = lambda a, b: tuple(i+j for i,j in zip(a,b))
    md5 = lambda x: hashlib.md5(x.encode()).hexdigest()[:4]
    free = lambda x: {k: v > 'a' for k, v in zip(((-1,0), (1,0), (0,-1), (0,1)), md5(x))}
    def pos(x: str):
        freq = Counter(x)
        return (freq.get('D',0)-freq.get('U',0), freq.get('R',0)-freq.get('L',0))
        

    dim = (4,4)
    room = {(i,j) for i in range(dim[0]) for j in range(dim[0])}
    end = sorted(room)[-1]

    # Part 1
    if True:
        state = {''}
        while True:  # Breadth First Search (BFS)
            state_ = set()
            for path in state:
                loc = pos(path)
                for d in {xy for xy, v in free(data+path).items() if v and plus(loc, xy) in room}:
                    state_.add(path + direction[d])
            state = state_
            if (p1 := {k for k in state if pos(k) == end}):
                break
            if len(state) == 0:
                raise Exception('No path.')
        print(f"A1: {next(iter(p1))}")

    # Part 2
    state = {''}
    while True:  # Breadth First Search (BFS)
        state_ = set()
        for path in state:
            loc = pos(path)
            for d in {xy for xy, v in free(data+path).items() if v and plus(loc, xy) in room}:
                state_.add(path + direction[d])
        if (end_ := {k for k in state_ if pos(k) == end}):
            best = end_
            state_ -= end_
        state = state_
        if len(state) == 0:
            break
    print(f"A2: {len(next(iter(best)))}")

if __name__ == '__main__':
    main()
