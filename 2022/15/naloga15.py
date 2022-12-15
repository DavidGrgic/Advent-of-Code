# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
#import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    env = 'd'
    # Read
    data = {}
    with open(env + '.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(':')
            k = tuple(int(i) for i in da[0].replace('Sensor at x=', '').replace(' y=', '').split(',')[::-1])
            v = tuple(int(i) for i in da[1].replace(' closest beacon is at x=', '').replace(' y=', '').split(',')[::-1])
            data.update({k:v})

    # Part 1
    y = {'t': 10}.get(env, 2000000)
    if True:
        ranges = set()
        for k, v  in data.items():
            ran = abs(k[0]-v[0]) + abs(k[1]-v[1])
            off = ran - abs(k[0]-y)
            ranges |= set(range(k[1]-off, k[1]+off))
        print(f"A1: {len(ranges)}")

    ab = lambda x: (x[0]+x[1], x[0]-x[1])
    yx = lambda x: ((x[0]+x[1]) /2, (x[0]-x[1]) /2)

    # Part 2
    poli = []
    for k, v  in data.items():
        _k = ab(k)
        _r = abs(k[0]-v[0]) + abs(k[1]-v[1])
        poli +=  [[(_k[0]-_r, _k[0]+_r), (_k[1]-_r, _k[1]+_r)]]
    poli = [[(max(i[0][0], 0), min(i[0][1], 4*y)), (max(i[1][0], -2*y), min(i[1][1], 2*y))] for i in poli]  # Fix overrange
    _poli = [i for i in poli if i[0][1] > i[0][0] and i[1][1] > i[1][0]]  # Remove empty
    poli = [_poli[0]]
    for j in _poli:
        vsebovan = False
        for i in poli:
            if j[0][0] >= i[0][0] and j[0][1] <= i[0][1] and j[1][0] >= i[1][0] and j[1][1] <= i[1][1]:
                vsebovan = True
                break
        if not vsebovan:
            poli += [j]
    i = 0
    while i < len(poli):
        j = i + 1
        while j < len(poli):
            if poli[i][0] == poli[j][0]:
                po = sorted([poli[i][1], poli[j][1]])
                if po[1][0] - po[0][1] <= 1:
                    poli[i] = [poli[i][0], (po[0][0], po[1][1])]
                    poli = poli[:j] + poli[j+1:]
                else:
                    j += 1
            elif poli[i][1] == poli[j][1]:
                po = sorted([poli[i][0], poli[j][0]])
                if po[1][0] - po[0][1] <= 1:
                    poli[i] = [(po[0][0], po[1][1]), poli[i][1]]
                    poli = poli[:j] + poli[j+1:]
                else:
                    j += 1
            else:
                j += 1
        i += 1
    _ab = tuple({j for i in poli for j in i[r]} for r in range(2))
    _ab = tuple({i+1 for i in _ab[r] if i+2 in _ab[r]} for r in range(2))
    _yx = {yx((a,b)) for a in _ab[0] for b in _ab[1]}
    _yx = {tuple((int(i[0]), int(i[1]))) for i in _yx if i[0] % 1 == 0 and i[1] % 1 == 0 and 0 <= i[0] <= 2*y and 0 <= i[1] <= 2*y}
    _yx = sorted(_yx, key = lambda x: abs(x[0]-y) + abs(x[1]-y))     # Bolj verjetni so rezultati bolj na sredi prostora
    print(f"A2, sorted by probability: {[i[0] + 4000000 * i[1] for i in _yx]}")

if __name__ == '__main__':
    main()
