﻿# -*- coding: utf-8 -*-
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
_img_map = {0: '.', 1: '#', 2:'*'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img, offset

def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split()
            data += [(da[0], int(da[1]), da[2][1:-1])]

    smer = {'R': (0,1), 'D': (1,0), 'L': (0,-1), 'U': (-1,0)}
    plus = lambda i, j, m=1: (i[0]+m*j[0], i[1]+m*j[1])

    def flood_out(field: np.array, what: set = {0}):
        fill = k = field.max() + 1
        field_ = np.full((field.shape[0]+2, field.shape[1]+2), fill)
        field_[1:-1,1:-1] = field.copy()
        while True:
            flood = np.where(field_ == k)
            if flood[0].shape[0] == 0:
                break
            k += 1
            for i, j in zip(*flood):
                for s in smer.values():
                    i_, j_ = plus((i, j), s)
                    if 0 <= i_ < field_.shape[0] and 0 <= j_ < field_.shape[1] and field_[i_, j_] in what:
                        field_[i_, j_] = k
        return field_[1:-1,1:-1] < fill

    def vmes(ij, ij_):
        res = [ij]
        if ij[0] == ij_[0]:
            d = 1
        elif ij[1] == ij_[1]:
            d = 0
        else:
            raise AssertionError
        dif = ij_[d] - ij[d]
        for _ in range(abs(dif)):
            x = list(res[-1])
            x[d] += int(np.sign(dif))
            res.append(tuple(x))
        return res

    # Part 1
    if True:
        pot = [(0,0)]
        for dat in data:
            for _ in range(dat[1]):
                pot.append(plus(pot[-1], smer[dat[0]]))
        bazen, off = _dict2img({i:1 for i in pot})
        bazen = flood_out(bazen)
        print(f"A1: {bazen.sum()}")

    # Part 2
    data = [(int(i[-1][-1]), int('0x' + i[-1][1:-1].upper(), 16)) for i in data]
    inv = {'R': 0, 'D': 1, 'L': 2, 'U': 3}
    smer = {inv[k]: v for k, v in smer.items()}

    pot = [(0,0)]
    for i, dat in enumerate(data):
        pot.append(plus(pot[-1], smer[dat[0]], dat[1]))
    iii = sorted({i[0] for i in pot})
    jjj = sorted({i[1] for i in pot})
    vogal = {plus((2*i,2*j), s): plus((ii, jj), s) for i, ii in enumerate(iii) for j, jj in enumerate(jjj) for s in {(0,0), (0,1), (1,0), (1,1)}}
    vogal_inv = {v: k for k, v in vogal.items()}
    bazen = np.zeros((2*len(iii), 2*len(jjj)), dtype = int)
    pott = [vogal_inv[p] for p in pot]
    for k in range(len(pott) - 1):
        tocke = vmes(pott[k], pott[k+1])
        for t in tocke:
            bazen[t] = 1
    bazen = flood_out(bazen)
    ploscina = 0
    for i in range(bazen.shape[0]-1):
        for j in range(bazen.shape[1]-1):
            if bazen[(i,j)] == 0:
                continue
            ii, jj = vogal[(i,j)]
            ii_, jj_ = vogal[(i+1,j+1)]
            ploscina += (ii_ - ii) * (jj_ - jj)
    print(f"A2: {ploscina}")

if __name__ == '__main__':
    main()
