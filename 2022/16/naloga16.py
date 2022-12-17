# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(';')
            kn = da[0].split(' has flow rate=')
            k = kn[0].replace('Valve ','')
            m = da[1].replace(' tunnels lead to valves ', '').replace(' tunnel leads to valve ', '').split(', ')
            data.update({k: (int(kn[1]), set(m))})

    G = nx.DiGraph()
    G.add_edges_from([(k, i) for k, v in data.items() for i in v[1]])

    def delaj(obiskani, ventili, t = 0):
        izpust = obiskani[-1], t, data[obiskani[-1]][0] * max((tt - t),0)
        res = {(izpust,)}
        for v in ventili - set(obiskani):
            dist = len(nx.shortest_path(G, obiskani[-1], v))   # Ker bomo vedno odprli ventil kamor bomo sli, vzamemo eno razdaljo vec, torej kar stevilo vozlisc
            if t + dist >= tt:
                continue
            sub = delaj(obiskani + [v], ventili, t + dist)
            res |= {(izpust,) + i for i in sub}
        return set((next(iter(sorted(res, key = lambda x: sum(i[2] for i in x), reverse = True))),))

    start = 'AA'

    # Part 1
    if True:
        tt = 30
        ventili = {k for k, v in data.items() if v[0] != 0}
        pot = next(iter(delaj([start], ventili)))
        p1 = sum(i[2] for i in pot)
        print(f"A1: {p1}")

    # Part 2
    tt = 26
    ventili = {k for k, v in data.items() if v[0] != 0}
    komb = set()
    for k in product(range(2), repeat = len(ventili)):
        komb |= {tuple(sorted(tuple(v for i, v in zip(k, ventili) if i == r) for r in range(2)))}
    max_izp = 0
    max_pot = ()
    for kom in komb:
        pot = ();
        for ko in kom:
            po = next(iter(delaj([(start)], set(ko))))
            pot += (po,)
        izp = sum(i[2] for p in pot for i in p)
        if izp > max_izp:
            max_pot = pot
        max_izp = max(max_izp, izp)
#        print(kom, izp, max_izp)
#    print(max_pot)
    print(f"A2: {max_izp}")

if __name__ == '__main__':
    main()