# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from collections import Counter
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
    wall = set()
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            for i, v in enumerate(ln.replace('\n', '')):
                if v == '#':
                    wall.add((c,i))
                    continue
                data.add((c,i))
                if v == 'S':
                    start = (c,i)
                elif v == 'E':
                    end = (c,i)
    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])
    dist = lambda a, b: abs(a[0]-b[0]) + abs(a[1]-b[1])
    save_t = 50 if len(data) < 100 else 100

    # Part 1
    dat = [(ij, plus(ij, s)) for ij in data for s in {(1,0), (0,1)} if plus(ij, s) in data]
    G0 = nx.Graph()
    G0.add_edges_from(dat)
    pot0 = nx.shortest_path(G0, start, end)
    if True:
        cheat = [[(ij, plus(ij,s)) for s in ss] for ij in wall for ss in {((1,0),(-1,0)), ((0,1), (0,-1))} if (plus(ij, ss[0]) in data and plus(ij, ss[1]) in data)]
        p1 = []
        for ch in cheat:
            G = nx.Graph()
            G.add_edges_from(dat + ch)
            pot = nx.shortest_path(G, start, end)
            if (diff := len(pot0) - len(pot)) > 0:
                p1.append(diff)
        print(f"A1: {sum(v for k, v in Counter(p1).items() if k >= save_t)}")

    # Part 2
    """ Part 1 can be better solved below method, replacing 20 picoseconds limit with 2 """
    assert len([p for p in nx.shortest_simple_paths(G0, start, end)]) == 1  # Only one valid path if no cheat?
    cheat = {(i, i+j+1) for i,n in enumerate(pot0) for j,m in enumerate(pot0[i+1:]) if (d:=dist(n,m)) <= j+1-save_t and d <= 20}
    print(f"A2: {len(cheat)}")

if __name__ == '__main__':
    main()
