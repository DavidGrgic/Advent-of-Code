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
    data = set()
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            for j, v in enumerate(ln.replace('\n', '')):
                if v == '#':
                    continue
                elif v == 'S':
                    start = (c,j)
                elif v == 'E':
                    end  = (c,j)
                data.add((c,j))

    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])
    cross = {(0,1): (1,0), (0,-1): (-1,0), (1,1): (0,-1), (1,-1): (0,1), (2,1): (-1,0), (2,-1): (1,0), (3,1): (0,1), (3,-1): (0,-1)}
    
    def score(pot):
        ret = 0
        for i in range(len(pot)-1):
            if len(pot[i]) <= 2 or len(pot[i+1]) <= 2:
                continue
            if pot[i][2] != pot[i+1][2]:
                ret += 1000
            else:
                ret += 1
        return ret

    # Part 1
    if True:
        dat = [((i,j,0), (i,j+1,0), 1) for i,j in data if (i,j+1) in data]  # dim 0: pomik v desno (east)
        dat += [((i,j,1), (i+1,j,1), 1) for i,j in data if (i+1,j) in data]  # dim 1: pomik v dol
        dat += [((i,j,2), (i,j-1,2), 1) for i,j in data if (i,j-1) in data]  # dim 2: pomik v levo
        dat += [((i,j,3), (i-1,j,3), 1) for i,j in data if (i-1,j) in data]  # dim 1: pomik v gor
        dat += [((i,j,d), (i,j,(d+d_) % 4), 1000) for i,j in data for d in range (4) for d_ in {-1, 1} if plus((i,j), cross[d,d_]) in data]  # zasuk
        dat += [(start, start + (0,), 0)]
        dat += [(end + (i,), end, 0) for i in range(4)]
        G = nx.DiGraph()
        G.add_weighted_edges_from(dat)
        pot = nx.shortest_path(G, start, end, 'weight')
        p1 = score(pot)
        print(f"A1: {p1}")

    # Part 2
    poti = []
    for po in nx.shortest_simple_paths(G, start, end, weight='weight'):
        sc = score(po)
        if sc != p1:
            break
        poti.append(po)
    p2 = {i[:2]for p in poti for i in p}
    print(f"A2: {len(p2)}")

if __name__ == '__main__':
    main()
