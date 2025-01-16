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
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    spread = {i: 0 for i in product(*(((0,1),) * 5))}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                continue
            elif ln.startswith(tmp:='initial state: '):
                data = {i for i, v in enumerate(ln[len(tmp):]) if v == '#'}
            else:
                match ln.split(' => '):
                    case x, '#':
                        spread.update({tuple(1 if i == '#' else 0 for i in x): 1})
    spread = {frozenset(i-2 for i, j in enumerate(k) if j == 1): v for k, v in spread.items()}

    # Part 1
    if True:
        dat = data.copy()
        for _ in range(20):
            dat = {i for i in range(min(dat)-2, max(dat)+3) if spread[frozenset(j for j in range(-2,3) if i+j in dat)]}
        print(f"A1: {sum(dat)}")

    # Part 2
    nn = 50000000000
    seq = [tuple(sorted(dat := data.copy()))]
    while len(seq) < 3 or not (len({len(i) for i in seq[-3:]}) == 1 and len(diff := {tuple(b-a for b,a in zip(seq[-i-1], seq[-i-2])) for i in range(2)}) == 1):
        seq.append(tuple(sorted(dat := {i for i in range(min(dat)-2, max(dat)+3) if spread[frozenset(j for j in range(-2,3) if i+j in dat)]})))
    p2 = {i + d * (nn-len(seq)+1) for i, d in zip(seq[-1], next(iter(diff)))}
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()
