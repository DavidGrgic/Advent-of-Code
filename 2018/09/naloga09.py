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
    players = 404; marbles = 71852
    #players = 10; marbles = 1618
    #players = 9; marbles = 25

    def game(players, marbles):
        player = {}
        seq = {0: [0,0]}
        current = 0
        for marble in range(1, marbles+1):
            if marble % 23 == 0:
                for _ in range(8):
                    current, nxt = seq[current_ := current]
                seq[current][1] = nxt
                seq[nxt][0] = current
                current = nxt
                del seq[current_]
                ply = ((marble - 1) % players) + 1
                player.update({ply: player.get(ply, set()) | {marble, current_}})
            else:
                _, current = seq[prv := current]
                _, nxt = seq[current]
                seq.update({current: [prv if prv != current else marble, marble], marble: [current, nxt], nxt: [marble, seq[nxt][1] if nxt != current else marble]})
                current = marble
        return {k: sum(v) for k, v in player.items()}

    # Part 1
    if True:
        p1 = game(players, marbles)
        print(f"A1: {max(p1.values())}")

    # Part 2
    p2 = game(players, 100*marbles)
    print(f"A2: {max(p2.values())}")

if __name__ == '__main__':
    main()
