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
def plot(data, mapper: dict = {0: '.', 1: '#'}, default: dict = {set: 1, dict: 0}):
    if isinstance(data, set):
        data = {k: default[set] for k in data}
    if isinstance(data, dict):
        offset = tuple(int(min(i[j] for i in data.keys())) for j in range(2))
        img = np.zeros(tuple(int(max(i[j] for i in data.keys())-offset[j])+1 for j in range(2))).astype(int) + default[dict]
        img[tuple(tuple(int(i[j]-offset[j]) for i in data.keys()) for j in range(2))] = list(data.values())
        data = img
    print('\n'+'\n'.join([''.join(mapper.get(i,'?') for i in j) for j in data]))

def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for l, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += [tuple(int(i) for i in ln.split(','))]

    area = lambda x, y: (abs(x[0]-y[0])+1) * (abs(x[1]-y[1])+1)

    # Part 1
    if True:
        rec = [(data[i], data[j]) for i in range(len(data)) for j in range(i+1, len(data))]
        rec = {ij: area(*ij) for ij in rec}
        print(f"A1: {max(rec.values())}")

    # Part 2
    def compress(dim):
        val = sorted({i[dim] for i in data})
        val_ = val[:1]
        for v in val[1:]:
            if v > (v_ := val_[-1] + 1):
                val_.append(v_)
            val_.append(v)
        return {k: v for k, v in enumerate(val_)}

    plus = lambda x, y: (x[0] + y[0], x[1] + y[1])

    x = compress(0)  # key is new position, value is original position
    y = compress(1)
    x_ = {v: k for k, v in x.items()}  # key is original position, value is new position
    y_ = {v: k for k, v in y.items()}
    dat = [(x_[d[0]], y_[d[1]]) for d in data]
    border = [dat[-1]]
    for d in dat:
        if border[-1][0] == d[0]:
            sig = 1 if d[1] > border[-1][1] else -1
            border += [(d[0], border[-1][1] + sig * (i+1)) for i in range(abs(border[-1][1] - d[1]))]
        elif border[-1][1] == d[1]:
            sig = 1 if d[0] > border[-1][0] else -1
            border += [(border[-1][0] + sig * (i+1), d[1]) for i in range(abs(border[-1][0] - d[0]))]
        else:
            raise ValueError()
    border = border[:-1]
    # Flood
    sea = set(border)
    for side in (1, -1):
        inf = False
        for b in range(len(border) - 1):
            if border[b][1] == border[b+1][1]:
                flood = (border[b][0], border[b][1] - side * (border[b+1][0] - border[b][0]))
            else:
                flood = (border[b][0] + side * (border[b+1][1] - border[b][1]), border[b][1])
            if flood in sea:
                continue
            flood = {flood}
            while True:
                flood_ = set()
                for f in flood:
                    for d in {(1,0), (-1,0), (0,1), (0,-1)}:
                        new = plus(f, d)
                        if new not in flood and new not in sea:
                            flood_.add(new)
                flood |= flood_
                if any(f[i] < 0 for f in flood for i in range(2)):
                    inf = True
                    break
                if not flood_:
                    break
            if inf:
                break
            sea |= flood
    rec = [(dat[i], dat[j]) for i in range(len(dat)) for j in range(i+1, len(dat))]
    valid = {}
    for a, b in rec:
        ii = sorted([a[0], b[0]])
        jj = sorted([a[1], b[1]])
        lake = {(i,j) for i in range(ii[0], ii[1]+1) for j in range(jj[0], jj[1]+1)}
        if not all(l in sea for l in lake):
            continue
        valid[(a,b)] = area(*((x[a[0]], y[a[1]]), (x[b[0]], y[b[1]])))
    print(f"A2: {max(valid.values())}")

if __name__ == '__main__':
    main()
