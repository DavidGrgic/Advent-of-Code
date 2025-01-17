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
        for c, ln in enumerate(file):
            data.extend(int(i) for i in ln.replace('\n', '').split())

    deepsum = lambda x: sum(sum(i) if isinstance(i, tuple) else deepsum(i) for i in x)

    def unpack(niz: list[int]):
        nodes = niz[0]
        metas = niz[1]
        niz_ = niz[2:]
        tree = []
        for _ in range(nodes):
            tree_, niz_ = unpack(niz_)
            tree.append(tree_)
        tree.append(tuple(niz_[:metas]))
        niz_ = niz_[metas:]
        return tree, niz_

    # Part 1
    p1, _ = unpack(data)
    print(f"A1: {deepsum(p1)}")

    # Part 2
    def checksum(tree):
        node = {i+1: v for i, v in enumerate([i for i in tree if isinstance(i, list)])}
        idx_dat = [i for i in tree if isinstance(i, tuple)][0]
        ret = 0
        if len(node) > 0:
            for i in idx_dat:
                tree_ = node.get(i)
                if tree_ is not None:
                    ret += checksum(tree_)
        else:
            ret = sum(idx_dat)
        return ret

    p2 = checksum(p1)
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
