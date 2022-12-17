# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
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


    def poti(obiskani, odprti = set(), t0 = 0, data = data):
        vv = obiskani[-1]
        pot = set()
        for i, d in dat[vv][1].items():# - set(obiskani[:-2]):
            for odpri in {False} if vv in odprti else {True, False}:
                if not odpri and i in obiskani[-2:]:
                    continue   # Nisma smisla iti k ventilu, ga ne odpreti in se vrniti nazaj
                _t = t0 + odpri
                izpust = odpri * dat[vv][0] * max((tt - _t),0)
                if _t+d >= tt-1 or odprti | ({vv} if odpri else set()) == set(dat)-{start}:
                    pot |= {((vv, odpri, izpust, _t),)}
                else:
                    po = poti(obiskani + [i], odprti | ({vv} if odpri else set()), _t+d)
                    pot |= {((vv, odpri, izpust, _t),) + i for i in po}
        return set((next(iter(sorted(pot, key = lambda x: sum(i[2] for i in x), reverse = True))),)) if len(pot) > 0 else pot

    def comp(vv, da):
        res = {}
        for v in da[vv[-1]][1] - set(vv):
            if da[v][0] == 0:
                dis = comp(vv + [v], da)
                res |= {k: d+1 for k, d in dis.items()}
            else:
                res.update({v: 1})
        return res

    start = 'AA'
    # Part 1
    tt = 30
    if False:
        dat = {}
        for k in {k for k, v in data.items() if v[0] != 0} | {start}:
            dis = comp([k], data)
            dat.update({k: (data[k][0], dis)})
        p1 = poti([(start)])
        print(f"A1: {max([sum(i[2] for i in p) for p in p1])}")

    # Part 2
    tt = 26
    ventili_izp = {k: v[0] for k, v in data.items() if v[0] != 0}
    ventili = ventili_izp.keys()
    komb = set()
    for k in product(range(2), repeat = len(ventili)):
        komb |= {tuple(sorted(tuple(v for i, v in zip(k, ventili) if i == r) for r in range(2)))}
    komb = sorted(komb, key = lambda x: (abs(len(x[0])-len(x[1])), abs(sum(ventili_izp[i] for i in x[0]) - sum(ventili_izp[i] for i in x[1]))))
    max_izp = 0
    for ko in komb:
        re = (); izp = 0
        for r in range(2):
            da = {k: v if k in ko[r] else (0,v[1])  for k, v in data.items()}
            dat = {}
            for k in {k for k, v in da.items() if v[0] != 0} | {start}:
                dis = comp([k], da)
                dat.update({k: (data[k][0], dis)})
            po = poti([(start)], data = da)
            izp += max([sum(i[2] for i in p) for p in po]) if len(po) > 0 else 0
            re += (ko[r],)
        max_izp = max(max_izp, izp)
        print(re, izp, max_izp)
    print(f"A2: {max_izp}")

if __name__ == '__main__':
    main()
