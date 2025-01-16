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
    split = lambda x: tuple(int(i) for i in x.split(','))[::-1]
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            da = ln.replace('\n', '').replace('>', '').replace('position=<', '').split('velocity=<')
            data.update({split(da[0]): split(da[1])})

    position = lambda t: {tuple(i+t*v for i, v in zip(xy,vl)) for xy, vl in data.items()}

    def score(dat):
        pt = [{ij[k] for ij in dat} for k in range(2)]
        return sum(max(i) - min(i) for i in pt)

    # Part 1
    if True:
        best = {}
        for t in range(10**9):
            pos = position(t)
            sco = score(pos)
            if len(best) == 0 or sco <= min(i[0] for i in best.values()):
                best.update({t: (sco, pos)})
                best_sco = sco
            if sco > 2 * best_sco:
                break
        print("A1:")
        plot(sorted(best.values())[0][-1], {0: ' ', 1: '#'})

    # Part 2
    print(f"A2: {sorted(best.items(), key=lambda item: item[1])[0][0]}")

if __name__ == '__main__':
    main()
