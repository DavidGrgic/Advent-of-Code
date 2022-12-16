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

    tt = 30

    def poti(obiskani, odprti = set(), t0 = 0):
        vv = obiskani[-1]
        pot = set()
        for i, d in dat[vv][1].items():# - set(obiskani[:-2]):
            for odpri in {False} if vv in odprti else {True, False}:
                if not odpri and i in obiskani[-2:]:
                    continue   # Nisma smisla iti k ventilu, ga ne odpreti in se vrniti nazaj
                _t = t0 + odpri
                izpust = odpri * dat[vv][0] * max((tt - _t),0)
                if _t+d >= tt-1 or set(obiskani) == set(dat):
                    pot |= {((vv, odpri, izpust, _t),)}
                else:
                    po = poti(obiskani + [i], odprti | ({vv} if odpri else set()), _t+d)
                    pot |= {((vv, odpri, izpust, _t),) + i for i in po}
        return set((next(iter(sorted(pot, key = lambda x: sum(i[2] for i in x), reverse = True))),)) if len(pot) > 0 else pot

    def comp(vv):
        res = {}
        for v in data[vv[-1]][1] - set(vv):
            if data[v][0] == 0:
                dis = comp(vv + [v])
                res |= {k: d+1 for k, d in dis.items()}
            else:
                res.update({v: 1})
        return res

    start = 'AA'
    dat = {}
    for k in {k for k, v in data.items() if v[0] != 0} | {start}:
        dis = comp([k])
        dat.update({k: (data[k][0], dis)})
    # Part 1
    if True:
        p1 = poti([(start)])
        print(f"A1: {max([sum(i[2] for i in p) for p in p1])}")

    # Part 2
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
