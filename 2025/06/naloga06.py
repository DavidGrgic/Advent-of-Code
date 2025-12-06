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
            data += [ln]
    oper_ = data[-1]
    oper = oper_.split()
    data = data[: -1]
    
    
    def calc(dat):
        p = []
        for d, o in zip(dat, oper):
            match o:
                case '+':
                    p.append(sum(d))
                case '*':
                    p.append(math.prod(d))
                case _:
                    raise RuntimeError()
        return p
    
    # Part 1
    if True:
        dat = [i.split() for i in data]
        dat = [[int(dat[j][i]) for j in range(len(dat))] for i in range(len(dat[0]))]
        p1 = calc(dat)
        print(f"A1: {sum(p1)}")

    # Part 2
    index = [i for i, v in enumerate(oper_) if v != ' '] + [len(oper_) + 1]
    dat=[]
    for i in range(len(index)-1):
        da = []
        for j in range(index[i], index[i+1]-1):
            da.append(int(''.join(data[l][j] for l in range(len(data)))))
        dat.append(da)
    p2 = calc(dat)
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()
