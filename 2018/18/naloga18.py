# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from collections import Counter
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
    mapper = {'.': 0, '|': 1, '#': 2}
    
    data = {}
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            data.update({(i,j): mapper[v] for j, v in enumerate(ln.replace('\n', ''))})

    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])
    direction = {i for i in product(range(-1,2), range(-1,2))} - {(0,0)}

    def cycle(dat):
        dat_ = dat.copy()
        for xy, v in dat.items():
            neighbour = Counter(dat[xy_] for d in direction if (xy_:=plus(xy,d)) in dat)
            match v:
                case 0:
                    if neighbour.get(1,0) >= 3:
                        dat_[xy] = 1
                case 1:
                    if neighbour.get(2,0) >= 3:
                        dat_[xy] = 2
                case 2:
                    if not (neighbour.get(1,0) and neighbour.get(2,0)):
                        dat_[xy] = 0
        return dat_
                        
    # Part 1
    if True:
        dat = data.copy()
        for _ in range(10):
            dat = cycle(dat)
        p1 = Counter(dat.values())
        print(f"A1: {p1[1]*p1[2]}")

    # Part 2
    nnn = 1000000000
    dat = data.copy()
    seq = [dat]
    while True:
        dat = cycle(dat)
        if any(chk := [dat == s for s in seq]):
            break
        seq.append(dat)
    offset = chk.index(True)
    freq = len(seq) - offset
    idx = (nnn - offset) % freq
    dat = seq[offset + idx]
    p2 = Counter(dat.values())
    print(f"A2: {p2[1]*p2[2]}")

if __name__ == '__main__':
    main()
