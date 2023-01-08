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
_img_map = {0: ' ', 1: '.'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,i) for i in j) for j in x]))
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(object)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

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
    zacetek = ()
    povezave = set()
    for k, v in data.items():
        if v == '#':
            continue
        elif v == '@':
            zacetek += (k,)
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

    def init(connections, starts):
        G = nx.Graph()
        G.add_edges_from(connections)
        nodes = {j for i in vrata.values() for j in i}
        G.add_edges_from(nodes)
        dostopni = ()
        for s in starts:
            kk = {}
            for k, v in kljuci.items():
                try:
                    nx.shortest_path(G, s, v)
                except nx.exception.NetworkXNoPath:
                    continue
                kk.update({k:v})
            dostopni += (kk,)
        G.remove_edges_from(nodes)
        return G, dostopni, {}

    def collect(start, keys):
        if len(keys) == 0:
            return tuple([s] for s in start)
        elif (start, keys) in cache:
            return cache[(start, keys)]
        res = None
        for _s, s in enumerate(start):
            for k in set(dostopni[_s]).intersection(keys):
                try:
                    _pot = nx.shortest_path(G, s, kljuci[k])
                except (nx.exception.NetworkXNoPath, nx.exception.NodeNotFound):
                    continue
                if res is not None and len(res[_s]) <= len(_pot):
                    continue
                nodes = vrata.get(k.upper(), set())
                G.add_edges_from(nodes)
                pot = collect(start[:_s] + (kljuci[k],) + start[_s+1:], tuple(_k for _k in keys if _k != k))
                G.remove_edges_from(nodes)
                _res = pot[:_s] + (_pot + pot[_s][1:],) + pot[_s+1:]
                if res is None or len(_res[_s]) < len(res[_s]):
                    res = _res
        cache.update({(start, keys): res})
        return res

    #_img_print(_dict2img({j:1 for i in povezave for j in i} | {next(iter(set.intersection(*(set(i) for i in v)))): k for k, v in vrata.items()} | {v: k for k, v in kljuci.items()} | {i:'@' for i in zacetek}))
    # Part 1
    if True:
        G, dostopni, cache = init(povezave, zacetek)
        pot = collect(zacetek, tuple(kljuci.keys()))
        print(f"A1: {sum(len(p)-1 for p in pot)}")

    # Part 2
    if max(k for i in povezave for j in i for k in j) <= 75:
        return
    odstrani = pove(plus(zacetek[0], (-1,-1)), plus(zacetek[0], (-1,0))) |\
        pove(plus(zacetek[0], (-1,0)), plus(zacetek[0], (-1,1))) |\
        pove(plus(zacetek[0], (0,-1)), plus(zacetek[0], (0,0))) |\
        pove(plus(zacetek[0], (0,0)), plus(zacetek[0], (0,1))) |\
        pove(plus(zacetek[0], (1,-1)), plus(zacetek[0], (1,0))) |\
        pove(plus(zacetek[0], (1,0)), plus(zacetek[0], (1,1))) |\
        pove(plus(zacetek[0], (-1,-1)), plus(zacetek[0], (0,-1))) |\
        pove(plus(zacetek[0], (0,-1)), plus(zacetek[0], (1,-1))) |\
        pove(plus(zacetek[0], (-1,0)), plus(zacetek[0], (0,0))) |\
        pove(plus(zacetek[0], (0,0)), plus(zacetek[0], (1,0))) |\
        pove(plus(zacetek[0], (-1,1)), plus(zacetek[0], (0,1))) |\
        pove(plus(zacetek[0], (0,1)), plus(zacetek[0], (1,1)))
    zacetki = tuple(plus(zacetek[0], i) for i in {(-1,-1), (-1,1), (1,-1), (1,1)})
    G, dostopni, cache = init(povezave - odstrani, zacetki)
    pot = collect(zacetki, tuple(kljuci.keys()))
    print(f"A2: {sum(len(p)-1 for p in pot)}")


if __name__ == '__main__':
    main()
