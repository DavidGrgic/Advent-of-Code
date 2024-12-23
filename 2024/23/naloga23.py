# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product
from functools import cache   # @cache
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
    link = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            link += [tuple(sorted(ln.split('-')))]
    comp = {j for i in link for j in i}
    conn = {k: tuple(i for i in comp if tuple(sorted({i,k})) in link) for k in comp}
    santa = {i for i in comp if i[0] == 't'}

    # Part 1
    if True:
        conn_ = {k: v for k, v in conn.items() if k in santa}
        tris = set()
        for s, v in conn_.items():
            for cc in combinations(v, 2):
                if cc[0] in conn[cc[1]]:
                    tris |= {tuple(sorted((s,) + cc))}
        print(f"A1: {len(tris)}")

    # Part 2
    @cache
    def isconn(included, candidate):
        todo = tuple(c for c in candidate if c not in included and all(i in conn[c] for i in included))
        if len(todo) <= 1:
            sub = {todo}
        else:
            sub = set()
            for co in todo:
                sub_ = isconn(tuple(sorted(included + (co,))), conn[co])
                sub |= {tuple(sorted((co,) + i)) for i in sub_}
            if True:  # Compress, we are interested just for longest
                sub = {sorted(sub, key = lambda x: len(x), reverse = True)[0]}  # interested on longest set
        return sub

    conn = {k: tuple(sorted((k,) + v)) for k, v in conn.items()}
    p2 = set()
    for com, sub in conn.items():
        p2 |= {tuple(sorted((com,) + i)) for i in isconn((com,), sub)}
    p2 = sorted(p2, key = lambda x: len(x), reverse = True)
    print(f"A2: {','.join(p2[0])}")

if __name__ == '__main__':
    main()
