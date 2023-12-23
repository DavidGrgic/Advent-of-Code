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
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
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
            data += [[i for i in ln]]
    data = np.array(data)

    plus = lambda x, y: (x[0]+y[0], x[1]+y[1])
    smer = {'>': (0,1), 'v': (1,0), '<': (0,-1), '^': (-1,0)}
    start = (0, ''.join(data[0,:]).find('.'))
    end = (data.shape[0]-1, ''.join(data[data.shape[0]-1,:]).find('.'))
    
    
    # Part 1
    if True:
        poti = set()
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                ij = (i,j)
                for s in (smer.values() if data[ij] == '.' else {smer.get(data[ij])}):
                    if s is None:
                        continue
                    ij_ = plus(ij, s)
                    if not (0 <= ij_[0] < data.shape[0] and 0 <= ij_[1] < data.shape[1]) or data[ij_] == '#':
                        continue
                    poti |= {(ij, ij_)}
        tocke = {i: v for i, v in enumerate({j for i in poti for j in i})}
        tocke_inv = {v: k for k, v in tocke.items()}
        G = nx.DiGraph()
        G.add_edges_from({tuple(tocke_inv[j] for j in i) for i in poti})
        p1 = [len(p)-1 for p in nx.all_simple_paths(G, tocke_inv[start], tocke_inv[end])]
        print(f"A1: {max(p1)}")

    # Part 2
    sosedi = {}
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            ij = (i,j)
            poti = set()
            for s in (smer if data[ij] != '#' else {}).values():
                ij_ = plus(ij, s)
                if not (0 <= ij_[0] < data.shape[0] and 0 <= ij_[1] < data.shape[1]) or data[ij_] == '#':
                    continue
                poti |= {ij_}
            if len(poti) > 0:
                sosedi.update({ij: poti})
    nodes = {start, end} | {k for k, v in sosedi.items() if len(v) > 2}
    nodes = {i: v for i, v in enumerate(nodes)}

    sort = lambda x: tuple(sorted(x))

    def potuj(source):
        nod_inv = {v: k for k, v in nodes.items()}
        poti = {}
        for p in sosedi[source]:
            po = [source, p]
            while True:
                if po[-1] in nodes.values():
                    poti.update({sort([nod_inv[po[0]], nod_inv[po[-1]]]): len(po)-1})
                    break
                sosed = sosedi[po[-1]]
                sosed = {i for i in sosed if i not in po}
                if len(sosed) == 0:
                    break
                elif len(sosed) == 1:
                    po.append(next(iter(sosed)))
                else:
                    raise AssertionError()
        return poti

    edges = {}
    for ij in set(nodes.values()) - {start, end}:
        edg = potuj(ij)
        edges.update(edg)
    G = nx.Graph()
    G.add_edges_from(edges.keys())
    start = next(iter(k for k, v in nodes.items() if v == start))
    end = next(iter(k for k, v in nodes.items() if v == end))
    p2 = []
    for kandidat in nx.all_simple_paths(G, start, end):
        wgt = 0
        for i in range(len(kandidat)-1):
            wgt += edges[sort([kandidat[i], kandidat[i+1]])]
        p2.append(wgt)
    print(f"A2: {max(p2)}")

if __name__ == '__main__':
    main()
