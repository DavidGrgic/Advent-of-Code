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


def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.lstrip('p=').split(' v=')
            data += [{k: [int(i) for i in v.split(',')][::-1] for k, v in zip(('p', 'v'), da)}]
    dim = (103, 101) if len(data) > 12 else (7, 11)
    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])

    def second(dat):
        dat_ = []
        for pv in dat:
            x, y = plus(pv['p'], pv['v'])
            dat_.append(pv | {'p': [x % dim[0], y % dim[1]]})
        return dat_

    # Part 1
    if True:
        dat=copy.deepcopy(data)
        for _ in range(100):
            dat = second(dat)
        pos = [d['p'] for d in dat]
        qua = [[p for p in pos if p[0] < dim[0]//2 and p[1] < dim[1]//2]]
        qua += [[p for p in pos if p[0] < dim[0]//2 and p[1] > dim[1]//2]]
        qua += [[p for p in pos if p[0] > dim[0]//2 and p[1] < dim[1]//2]]
        qua += [[p for p in pos if p[0] > dim[0]//2 and p[1] > dim[1]//2]]
        print(f"A1: {math.prod([len(q) for q in qua])}")

    # Part 2
    dat=copy.deepcopy(data)
    _img_print = lambda x: print('\n'+'\n'.join([''.join('#' if (j,i) in x else '.' for i in range(dim[1])) for j in range(0,dim[0],1)]))

    def tree(pos, size = 5):
        """ Expecting up or down oriented triangle of some size. """
        for p in pos:
            for d in {1,-1}:
                sub = set()
                for i in range(1, size):
                    for j in range(-i,i+1):
                        sub.add(plus(p, (i*d, j)))
                if all(k in pos for k in sub):
                    return p
        return False

    sec = 0
    while True:
        sec += 1
        dat = second(dat)
        pos = [tuple(d['p']) for d in dat]
        if (p := tree(pos, 4)):
            _img_print(pos)
            break
    print(f"A2: {sec}")

if __name__ == '__main__':
    main()
