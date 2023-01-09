# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '.'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

plus = lambda x, y: (x[0]+y[0], x[1]+y[1])
isportal = lambda x: len(x) == 2 and all('A' <= i <= 'Z' for i in x)

def main():
    # Read
    with open('t1.txt', 'r') as file:
        data = file.readlines()
    data = [i.replace('\n', '') for i in data]

    povezave = set()
    debelina = sum(i in {'.', '#'} for i in data[len(data) // 2]) // 2
    for i in range(2, len(data) - 2):
        for j in range(2, len(data[2])-2):
            if data[i][j] == '.':
                for d in {(0,1), (-1,0), (0,-1), (1,0)}:
                    _i = i+d[0]; _j = j+d[1]
                    if data[_i][_j] == '.':
                        povezave |= {tuple(sorted(((i,j), (_i,_j))))}
    #_img_print(_dict2img({i:1 for k in povezave for i in k}))
    portal = []
    portal.extend([(''.join(v), (2, i)) for i, v in enumerate(zip(*tuple(data[:2]))) if isportal(''.join(v))])  # Zunaj zgoraj
    portal.extend([(''.join(v), (len(data)-3, i)) for i, v in enumerate(zip(*tuple(data[len(data)-2:]))) if isportal(''.join(v))])  # Zunaj spodaj
    portal.extend([(v[:2], (i, 2)) for i, v in enumerate(data) if isportal(v[:2])])  # Zunaj levo
    portal.extend([(v[-2:], (i, len(data[2])-3)) for i, v in enumerate(data) if isportal(v[-2:])])  # Zunaj desno
    portal.extend([(''.join(v), (1+debelina, i)) for i, v in enumerate(zip(*tuple(data[2+debelina:4+debelina]))) if isportal(''.join(v))])  # Znotraj zgoraj

    portal = (lambda P = {i[0] for i in portal}: {k: tuple(sorted(i[1] for i in portal if i[0] == k)) for k in P})()
    assert (lambda P = {j for i in povezave for j in i}: all(i in P for v in portal.values() for i in v))()
    # Part 1
    if True:
        G = nx.Graph()
        G.add_edges_from(povezave | {i for i in portal.values() if len(i) == 2})
        pot = nx.shortest_path(G, portal['AA'][0], portal['ZZ'][0])
        print(f"A1: {len(pot)-1}")

    # Part 2
    dat=copy.deepcopy(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
