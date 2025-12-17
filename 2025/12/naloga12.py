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
    if isinstance(data, (set, frozenset)):
        data = {k: default[set] for k in data}
    if isinstance(data, dict):
        offset = tuple(int(min(i[j] for i in data.keys())) for j in range(2))
        img = np.zeros(tuple(int(max(i[j] for i in data.keys())-offset[j])+1 for j in range(2))).astype(int) + default[dict]
        img[tuple(tuple(int(i[j]-offset[j]) for i in data.keys()) for j in range(2))] = list(data.values())
        data = img
    print('\n'+'\n'.join([''.join(mapper.get(i,'?') for i in j) for j in data]))

def main():
    # Read
    shape = []
    tree = []
    shape_ = False
    with open('d.txt', 'r') as file:
        for l, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                shape_ = False
                continue
            if ln[-1] == ':':
                shape_ = True
                shape.append([])
                continue
            elif ':' in ln[:-1]:
                da = ln.split(':')
                tree += [(tuple([int(i) for i in da[0].split('x')][::-1]),
                         {i: int(v) for i, v in enumerate(da[-1].split())})]
            if shape_:
                shape[-1].append({i for i, v in enumerate(ln) if v == '#'})
    shape = tuple({(i, j) for i, v in enumerate(s) for j in v} for s in shape)

    def normalize(s):
        min_i = min(i for i, j in s)
        min_j = min(j for i, j in s)
        return {(i - min_i, j - min_j) for i, j in s}

    shape_variant = []
    for ss in shape:
        variants = set()
        for _ in range(2):
            ss = normalize({(-i, j) for i, j in ss})  # Flip
            s = ss.copy()
            for _ in range(4):
                s = normalize({(j, -i) for i, j in s})  # Rotate
                variants.add(frozenset(s))
        shape_variant.append(tuple(set(v) for v in variants))

    move = lambda s, x, y: {(i[0]+x, i[1]+y) for i in s}
    
    def build(area, gift):
        if sum(gift.values()) == 0:
            return [[()]]
        else:
            gf = {k for k, v in gift.items() if v}
            if area:
                xy = max(i[0] for i in area) + 2, max(i[1] for i in area) + 2
            else:
                xy = 1, 1
            nxt = {(g, i, x, y): a_s
                    for g in gf
                    for i, v in enumerate(shape_variant[g])
                    for x in range(xy[0])
                    for y in range(xy[1])
                    if (a_s := area | (s := move(v, x, y)))
                    and (not area or not area & s)
                    and max(i[0] for i in a_s) < dim[0]
                    and max(i[1] for i in a_s) < dim[1]
                    }
            res = []
            for k, a in nxt.items():
                # plot(a)
                g = gift.copy()
                g[k[0]] -= 1
                if (r := build(a, g)):
                    res += [[k] + i for i in r]
                    return res  # Comment this line if you would like to get all solutions
        return res

    # Part 1
    if True:
        p1 = []
        shape_dim = max(i[0] for v in shape_variant for s in v for i in s) + 1, \
            max(i[1] for v in shape_variant for s in v for i in s) + 1
        shape_len = {i: len(s) for i, s in enumerate(shape)}
        for dim, gift in tree:
            slots = (dim[0] // shape_dim[0]) * (dim[1] // shape_dim[1])
            if slots >= sum(gift.values()):
                p1.append(True)
                continue
            tiles = sum(v * shape_len[k] for k, v in gift.items())
            if math.prod(dim) < tiles:
                p1.append(False)
                continue
            area = set()
            p1.append(bool(build(area, gift)))
        print(f"A1: {sum(p1)}")

    # Part 2
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
