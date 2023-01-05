# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import networkx as nx
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    plus = lambda x, y: (x[0]+y[0],x[1]+y[1])
    pove = lambda x, y: {tuple(sorted([x,y]))}

    # Read
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            for i, l in enumerate(ln):
                data.update({(c,i): l})

    vrata = {}
    kljuci = {}
    povezave = set()
    for k, v in data.items():
        if v == '#':
            continue
        elif v == '@':
            zacetek = k
        elif 'a' <= v <= 'z':
            kljuci.update({v: k})
        for s in {(0,1), (-1,0), (0,-1), (1,0)}:
            _k = plus(k, s)
            _v = data.get(_k)
            if _v in {'#', None}:
                continue
            if 'A' <= v <= 'Z':
                vrata.update({v: vrata.get(v,set()) | pove(k, _k)})
            else:
                if not ('A' <= _v <= 'Z'):
                    povezave |= pove(k, _k)

    def collect(start, keys, nodes):
        if len(keys) == 0:
            return [start]
        G = nx.Graph()
        G.add_edges_from(nodes)
        res = []
        for k, v in keys.items():
            try:
                _pot = nx.shortest_path(G, start, v)
            except (nx.exception.NetworkXNoPath, nx.exception.NodeNotFound):
                continue
            pot = collect(v, {_k: v for _k, v in keys.items() if _k != k}, nodes | vrata.get(k.upper(), set()))
            res.append(_pot + pot[1:])
        return sorted(res, key = lambda x: len(x))[0]

    # Part 1
    if True:
        pot = collect(zacetek, kljuci, povezave)
        print(f"A1: {len(pot)-1}")
          
    
    # Part 2

    print(f"A2: {0}")


if __name__ == '__main__':
    main()
