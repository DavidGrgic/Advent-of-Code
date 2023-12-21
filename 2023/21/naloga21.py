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
_img_map = {0: '.', 1: 'O'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [1 if i == '#' else 0 for i in ln]
            r = ln.find('S')
            if r >= 0:
                start = (c,r)
            data += [da]
    data = np.array(data)
    ii = data.shape[0]
    jj = data.shape[1]

    plus = lambda x, y: (x[0]+y[0], x[1]+y[1])

    # Part 1
    if True:
        pot = np.zeros_like(data)
        pot[start] = 1
        for _ in range(64):
            idx = np.where(pot == 1)
            pot = np.zeros_like(data)
            for i,j in zip(*idx):
                for s in {(1,0), (-1,0), (0,1), (0,-1)}:
                    i_, j_ = plus((i,j), s)
                    if 0 <= i_ < data.shape[0] and 0 <= j_ < data.shape[1] and data[i_, j_] != 1:
                        pot[i_, j_] = 1
           #_img_print(pot)
        print(f"A1: {pot.sum()}")

    # Part 2
    exp = lambda ij, s: (lambda ij_ = plus(ij, s): set() if (ij_[0] % ii, ij_[1] % jj) in rock else {ij_})()
    rock = {(i, j) for i, j in zip(*np.where(data))}

    def p2(num, resitev, step, diff, order = 2):
        periods = (num - len(resitev)) // step + 1
        index = num - step * periods
        diff_ = resitev[index] - resitev[index-step]
        return resitev[index] + sum([diff_ + (i+1) * diff for i in range(periods)])
    
    pot = {start}
    resitev = []
    diff = None
    while True:
        resitev.append(len(pot))
        if len(resitev) % 65 == 0:
            print(len(resitev))
            for step in range(data.shape[0], len(resitev), data.shape[0]):   # Zelimo imeti vsaj dve tocki vec kot je order, zado da dobimo vsaj dva odvoda in pogledamo, če sta ista
                diff = np.diff(resitev[::-step][:2+2], 2)   # Pricakujemo vzorec v kvadratnem narascanju stevila polj, zato n = 2. Zelimo imeti vsaj dva elementa več kot order funkcij (2+2)
                if len(diff) > 1 and len(set(diff)) == 1:
                    diff = int(next(iter(diff)))
                    break
            if isinstance(diff, int):
                break
        pot = {k for ij in pot for s in {(1,0), (-1,0), (0,1), (0,-1)} for k in exp(ij, s)}
    print(f"{step}, {diff}")
    print(p2(500, resitev, step, diff))
    print(p2(1000, resitev, step, diff))
    print(p2(5000, resitev, step, diff))
    print(f"A2: {p2(26501365, resitev, step, diff)}")

if __name__ == '__main__':
    main()
