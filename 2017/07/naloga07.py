# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#from functools import cache   # @cache
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    weight = {}
    link = {}
    disc = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' -> ')
            name, wei = da[0].split()
            weight.update({name: int(wei[1:-1])})
            if len(da) > 1:
                drzi = tuple(da[1].split(', '))
                link.update({i: name for i in drzi})
                disc.update({name: drzi})

    # Part 1
    if True:
        name = next(iter(weight))
        while name in link:
            name = link[name]
        print(f"A1: {name}")

    # Part 2
    def teze(name):
        return weight[name] + sum(teze(k) for k in disc.get(name, ()))

    data = {}
    for k, v in disc.items():
        w = [teze(i) for i in v]
        if len(set(w)) > 1:
            unbalance = sorted(Counter(w).items(), key=lambda item: item[1])[0][0]
            outlayer = v[w.index(unbalance)]
            correct = weight[outlayer] + next(iter(set(w) - {unbalance})) - unbalance
            data.update({outlayer: correct})
    for k, value in data.items():
        if not any(i in data for i in disc[k]):
            break
    print(f"A2: {value}")

if __name__ == '__main__':
    main()
