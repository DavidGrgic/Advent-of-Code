# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
from functools import cache   # @cache
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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += [ln]
    numkey = {'7': (0,0), '8': (0,1), '9': (0,2),
              '4': (1,0), '5': (1,1), '6': (1,2),
              '1': (2,0), '2': (2,1), '3': (2,2),
                          '0': (3,1), 'A': (3,2)}
    dirkey = {            '^': (0,1), 'A': (0,2),
              '<': (1,0), 'v': (1,1), '>': (1,2)}
    move = {'^': (-1,0), '<': (0,-1), 'v': (1,0), '>': (0,1)}

    move_ = {v:k for k,v in move.items()}
    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])
    neg = lambda a: (-a[0], -a[1])
    Gdir = nx.Graph()
    Gdir.add_edges_from([(m, [k for k, v in dirkey.items() if v == plus(p,s)][0]) for m, p in dirkey.items() for s in {(1,0), (0,1)} if plus(p,s) in dirkey.values()])
    Gnum = nx.Graph()
    Gnum.add_edges_from([(n, [k for k, v in numkey.items() if v == plus(p,s)][0]) for n, p in numkey.items() for s in {(1,0), (0,1)} if plus(p,s) in numkey.values()])

    @cache
    def push(state, sequence, depth):
        pushes = [sequence if d == depth else '' for d in range(depth+1)]
        if depth > 0:
            G, key_ = (Gnum, numkey) if depth == levels else (Gdir, dirkey)
            for target in sequence:
                best_pushes = best_state = None
                for pot in nx.shortest_simple_paths(G, state[depth], target):
                    state_, pushes_ = tuple(target if d == depth else v for d,v in enumerate(state)), pushes[:]
                    seq = ''.join(move_[plus(key_[pot[i+1]], neg(key_[pot[i]]))] if i < len(pot)-1 else 'A' for i in range(len(pot)))
                    state_, pu = push(state_, seq, depth-1)
                    for d in range(depth):
                        pushes_[d] += pu[d]
                    if best_pushes is None or len(pushes_[0]) < len(best_pushes[0]):
                        best_state, best_pushes = state_, pushes_
                state, pushes = best_state, best_pushes
        return state, pushes

    # Part 1
    if True:
        levels = 3
        p1 = {}
        for dat in data:
            state = ('A',) * (levels+1)
            state, pushes = push(state, dat, levels)
            p1.update({dat: pushes})
        print(f"A1: {sum(len(v[0]) * int(k[:-1]) for k, v in p1.items())}")

    # Part 2
    levels = 26
    p2 = {}
    for dat in data:
        state = ('A',) * (levels+1)
        state, pushes = push(state, dat, levels)
        p2.update({dat: pushes})
    print(f"A2: {sum(len(v[0]) * int(k[:-1]) for k, v in p2.items())}")

if __name__ == '__main__':
    main()
