# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():
    # Read
    data = {}
    with open('t.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(':')
            k = tuple(int(i) for i in da[0].replace('Sensor at x=', '').replace(' y=', '').split(',')[::-1])
            v = tuple(int(i) for i in da[1].replace(' closest beacon is at x=', '').replace(' y=', '').split(',')[::-1])
            data.update({k:v})

    # Part 1
    if False:
        dat=copy.deepcopy(data)
        ranges = set()
        y = 2000000
    #    y=10
        for k, v  in dat.items():
            ran = abs(k[0]-v[0]) + abs(k[1]-v[1])
            off = ran - abs(k[0]-y)
            ranges |= set(range(k[1]-off, k[1]+off))
        print(f"A1: {len(ranges)}")

    ab = lambda x: (x[0]+x[1], x[0]-x[1])
    yx = lambda x: ((x[0]+x[1]) /2, (x[0]-x[1]) /2)

    # Part 2
    dat=copy.deepcopy(data)
    poli = []
    y = 2000000
    y=10
    poli = [[(0,4*y), (-2*y,2*y)]]
    for k, v  in dat.items():
        _k = ab(k)
        _r = abs(k[0]-v[0]) + abs(k[1]-v[1])
        _poli = []
        for po in poli:
            _poli += [[(po[0][0], _k[0]-_r), (po[1][0], _k[1]-_r)]]
            _poli += [[(_k[0]-_r, _k[0]+_r), (po[1][0], _k[1]-_r)]]
            _poli += [[(_k[0]+_r, po[0][1]), (po[1][0], _k[1]-_r)]]
            _poli += [[(po[0][0], _k[0]-_r), (_k[1]-_r, _k[1]+_r)]]
            _poli += [[(_k[0]-_r, _k[0]+_r), (po[1][0], _k[1]-_r)]]
            _poli += [[(_k[0]+_r, po[0][1]), (po[1][0], _k[1]-_r)]]

    print(f"A2: {0}")

if __name__ == '__main__':
    main()
