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
    elevator = 1
    if True:  # Puzle
        # Index: 0: thulium, 1: plutonium, 2: strontium, 3: promethium, 4: ruthenium
        gen = (1, 1, 1, 3, 3)
        chip = (1, 2, 2, 3, 3)
    else:  # Test
        # Index: 0: hydrogen, 1: lithium
        gen = (2, 3)
        chip = (1, 1)

    assert len(gen) == len(chip), "Number of generators and elements should match."

    move2pos = lambda p, m: tuple(None if i in m else v for i, v in enumerate(p))

    def valid(position, num):
        if not all(position[c] == position[c-num] or all(position[g] != position[c] for g in range(num)) for c in range(num, 2*num) if position[c] is not None):  # Chip should have its own generator in same floor or there should be no generator in the floor
            return False
        return True

    def travel(initial_state: tuple):  # BFS
        num = len(initial_state) // 2
        cache = set()
        state = {initial_state}
        t = 0
        while not any(set(s) == {4} for s in state):
            cache |= state
            t += 1
            state_ = set()
            for pos in state:
                # Load elevator
                floor_asset = {i for i, v in enumerate(pos[:-1]) if v == pos[-1]}
                pos_ = {p for i in range(1, 3) for a in combinations(floor_asset, i) if valid(p := move2pos(pos, a), num)}  # Elevator should carry at least one and at most two assets
                # New floor
                for f in {k for k in range(1, 5) if abs(k-pos[-1]) == 1}:  # f: next floor
                    fpos_ = {tuple(f if i is None else i for i in p[:-1]) + (f,) for p in pos_}
                    state_ |= {p for p in fpos_ if valid(p, num) and p not in cache}
            state = state_
            if (state_len := len(state)) == 0:
                raise RuntimeError('No solution.')
            #print(f"At {t}, number of states: {state_len}")
        return t

    # Part 1:
    if True:
        p1 = travel(gen + chip + (elevator,))
        print(f"A1: {p1}")

    # Part 2
    # Add into 1st floor: elerium, dilithium
    gen += (1, 1)
    chip += (1, 1)
    p2 = travel(gen + chip + (elevator,))
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
