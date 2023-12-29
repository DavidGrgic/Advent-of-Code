# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
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
            ln = ln.replace('\n', '')
            da = ln.split(' @ ')
            data.append(tuple(tuple(int(j) for j in i.split(',')) for i in da))

    # Part 1
    if True:
        xy = (200000000000000, 400000000000000)
        p1 = 0
        for par in combinations(data, 2):
            k = [Fraction(i[-1][1], i[-1][0])  for i in par]
            n = [par[i][0][1] - par[i][0][0] * v for i, v in enumerate(k)]
            if k[0] == k[1]:   # parallel
                continue
            x = (n[1] - n[0]) / (k[0] - k[1])
            y = k[0] * x + n[0]
            t = [Fraction(x - p[0][0], p[1][0]) for p in par]
            if any(i < 0 for i in t):
                continue
            if all(xy[0] <= i <= xy[1] for i in {x,y}):
                p1+=1
        print(f"A1: {p1}")

    # Part 2
    # x, y, z, vx, vy, vz so začetne pozicije in hitrosti delca, ki ga ustrelimo
    # x_i, y_i, z_i, vx_i, vy_i, yz_i so začetne pozicije in hitrosti kepice i
    # Kjer se trčita delec in kepica, velja enako za vse tri dimenzije: x + t_i * vx = x_i + t_i * vx_i
    # Iz česar izpeljemo čas trka dalca s kepico i: t_i = (x_i - x) / (vx - vx_i)
    # Ter uporabimo ta čas da združio dve dimentiji, recimo x in y: (x_i - x) * (vy - vy_i) = (y_i - y) * (vx - vx_i)
    # Napisemo se enako enacbo za trk delca in kepice j, spet za isti dimenziji: (x_j - x) * (vy - vy_j) = (y_j - y) * (vx - vx_j)
    # Enacbi odstejemo, tako da odpade clen x * vx in dobimo: x * (vy_i - vy_j) - y * (vx_i - vx_j) - vx * (y_i - y_j) + vy * (x_i - x_j) = x_i * vy_i - x_j * vy_j - y_i * vx_i + y_j * vx_j
    # Imamo torej 6 neznank (x, y, z, vx, vy, vz) in potrebujemo 6 enačb. DObimo jih tako, da kombiniramo dva para dimenzij (tretji par ni neodvisen od prvih dveh) ter tri pare kepic
    dtype = 'int64'
    A = np.zeros((0,6), dtype = dtype)
    b = np.zeros(0, dtype = dtype)
    for d0, d1 in [(0,1), (0,2), (0,3)]:   # Prv in drugi delec
        for sx, sy in [(0,1), (0,2)]:   # Prva in druga spremelnjivka (osi so 0:x, 1:y, 2:z)
            a = np.zeros(6, dtype = dtype)
            a[sx] = data[d0][-1][sy] - data[d1][-1][sy]
            a[sy] = -(data[d0][-1][sx] - data[d1][-1][sx])
            a[sx+3] = -(data[d0][0][sy] - data[d1][0][sy])
            a[sy+3] = data[d0][0][sx] - data[d1][0][sx]
            A = np.append(A, a.reshape((1,-1)), axis = 0)
            b = np.append(b, np.array([  data[d0][0][sx] * data[d0][-1][sy]  -  data[d1][0][sx] * data[d1][-1][sy]  + data[d1][0][sy] * data[d1][-1][sx]  -  data[d0][0][sy] * data[d0][-1][sx]  ]))
    p2 = np.linalg.solve(A, b)
    print(f"A2: {int(p2[:3].sum().round(0))}")

if __name__ == '__main__':
    main()
