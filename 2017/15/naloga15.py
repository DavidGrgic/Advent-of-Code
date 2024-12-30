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
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            da = ln.replace('\n', '').split()
            data.update({da[1]: int(da[-1])})

    factor = {'A': 16807, 'B': 48271}
    data = {k: (v, factor[k]) for k, v in data.items()}

    def gen(n, value, factor):
        for _ in range(n):
            value = (value * factor) % 2147483647
            yield value

    def picky(n, value, factor, multi):
        i = 0
        while i < n:
            value = (value * factor) % 2147483647
            if value % multi == 0:
                i += 1
                yield value

    bit = 2**16
    # Part 1
    if True:
        nn = 40*10**6
        p1 = [(i+1,a,b) for i,(a,b) in enumerate(zip(gen(nn, *data['A']), gen(nn, *data['B']))) if a % bit == b % bit]
        print(f"A1: {len(p1)}")

    # Part 2
    multi = {'A': 4, 'B': 8}
    data = {k: v + (multi[k],) for k, v in data.items()}
    nn = 5*10**6
    p2 = [(i+1,a,b) for i,(a,b) in enumerate(zip(picky(nn, *data['A']), picky(nn, *data['B']))) if a % bit == b % bit]
    print(f"A2: {len(p2)}")

if __name__ == '__main__':
    main()
