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
            da = ln.replace('\n', '').split('>, r=')
            data.append((tuple(int(i) for i in da[0][5:].split(',')), int(da[1])))
    assert len(data) == len(data := set(data)), "Code is optimised to work with set... if nanorobots are duplicated by position and radius, code should be updated"

    distance = lambda a, b = (0,0,0): sum(abs(i-j) for i,j in zip(a,b))

    def explore(candidates, intersect = None, included = None):
        # ret vrne negativno število nanobotov, ki pokrivajo določen presek ter 
        # minimalno razdaljo od izhodišča, ki je v bistvu ena od mej prve osi (0),
        # odvisno, na kateri strani se nahajamo, oziroma 0, če je presek ravno čez izhodišče
        ret = [] if intersect is None else \
            [(included,
              0 if intersect[0][0] <= 0 and intersect[0][1] >= 0 
              else (intersect[0][0] if intersect[0][0] > 0 else -intersect[0][1]))]
        done = set()
        while (todo := candidates - done):
            nanobot = next(iter(todo))
            done.add(nanobot)
            if intersect is None:
                included = set()
                sub_intersect = nanobot
            else:
                sub_intersect = tuple((max(v[0], w[0]), min(v[1], w[1])) for v, w in zip(intersect, nanobot))
                if any(v[0] > v[1] for v in sub_intersect):
                    continue
            ret_ = explore(candidates - done, sub_intersect, included | {nanobot})
            done |= ret_[0]
            ret.append(ret_)
        return sorted(ret, key=lambda x: (-len(x[0]), x[1]))[0]

    # Part 1
    if True:
        strongest = [k for k in sorted(data, key=lambda i: i[-1], reverse=True)][0]
        p1 = [k for k in data if distance(strongest[0], k[0]) <= strongest[-1]]
        print(f"A1: {len(p1)}")

    # Part 2
    # Vsak nanobot je (v prostoru, kjer se merijo Manhaten razdalje) omejen z 'diamantom' s 8 trikotnimi stranicami, od katerih so paroma paralelene
    # Teh 8 stranic predstavlja 4 osi (a, b, c in d) kot:
    # a = x+y+z, b = x+y-z, c = x-y+z in d = x-y-z
    # Območja (rangi) posameznih nanobotov so v teh kordinatah opiasni kot ((a_min, a_max), (b_min, b_max), (c_min, c_max), (d_min, d_max))
    dat = {((x+y+z-r, x+y+z+r), (x-y+z-r, x-y+z+r), (x+y-z-r, x+y-z+r), (x-y-z-r, x-y-z+r)) for (x,y,z),r in data}
    p2 = explore(dat)
    print(f"A2: {p2[-1]}")

if __name__ == '__main__':
    main()
