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
            data.append(ln.replace('\n', ''))

    #data = ['abba[mnop]qrst']
    #data = ['abcd[bddb]xyyx']
    #data = ['aaaa[qwer]tyui']
    #data = ['ioxxoj[asdfgh]zxcvbn']
    #data = ['aba[bab]xyz']
    #data = ['xyx[xyx]xyx']
    #data = ['aaa[kek]eke']
    #data = ['zazbz[bzb]cdb']

    def parts(dat):
        i = 0
        base = []
        part = []
        while (i_ := dat[i:].find('[')) >= 0:
            _i = dat[i:].find(']')
            base.append(dat[i:i+i_])
            part.append(dat[i+i_+1:i+_i])
            i += _i + 1
        base.append(dat[i:])
        return base, part

    def is_abba(x, l = 4):
        return any(all(x[j] != x[j+1] for j in range(i, i+l//2-1)) and x[i+l//2-1] == x[i+l//2] and all(x[i+j] == x[i+l-j-1] for j in range(l//2)) for i in range(len(x)+1-l))
    
    def get_aba(x):
        return {x[i:i+3] for i in range(len(x)-2) if x[i] == x[i+2] and x[i] != x[i+1]}
    
    # Part 1
    if True:
        p1 = []
        for dat in data:
            ba, pa = parts(dat)
            p1.append(any(is_abba(b) for b in ba) and not any(is_abba(p) for p in pa))
        print(f"A1: {sum(p1)}")

    # Part 2
    p2 = []
    for dat in data:
        ba, pa = parts(dat)
        aba = {i for b in ba for i in get_aba(b)}
        bab = {i for p in pa for i in get_aba(p)}
        p2.append(bool(aba & {i[1] + i[:-1] for i in bab}))
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()
