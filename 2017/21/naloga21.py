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
    rule = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            in_, out_ = ln.split(' => ')
            d = len(in_.split('/')[0])
            if d not in rule:
                rule[d] = {}
            rule[d].update({tuple(sorted((i,j) for i, x in enumerate(in_.split('/')) for j, y in enumerate(x) if y=='#')):
                            tuple(sorted((i,j) for i, x in enumerate(out_.split('/')) for j, y in enumerate(x) if y=='#'))})

    def flip(fild: set[tuple], size: int, axis: int = 0):
        return fild.__class__(sorted((i,size-j-1) if axis % 2 else (size-i-1,j) for i,j in fild))

    def rotate(fild: set[tuple], size: int, num: int = 1):
        for _ in range(num % 4):
            fild = fild.__class__(sorted((j,i) for i,j in flip(fild, size, 1)))
        return fild

    # Expand rules by rorating and fliping
    for d, r in rule.items():
        r |= {rotate(k,d,-1): v for k,v in r.items()}
    for d, r in rule.items():
        r |= {flip(k,d,a):v for k,v in r.items() for a in range(2)}

    def expand(field, dim, nn = 2):
        ret = [len(field)]
        for _ in range(nn):
            div = 2 if dim % 2 == 0 else 3
            exp = {2:3, 3:4}[div]
            field = [(ii*exp+i, jj*exp+j) for ii in range(dim // div) for jj in range(dim // div) for i,j in rule[div][tuple(sorted((i%div, j%div) for i,j in field if i // div == ii and j // div == jj))]]
            dim = exp * (dim // div)
            ret.append(len(field))
        return ret

    field = [(0,1), (1,2), (2,0), (2,1), (2,2)]
    dim = max(j for i in field for j in i)+1
    # Part 1
    if True:
        p1 = expand(field, dim, 5)
        print(f"A1: {p1[-1]}")

    # Part 2
    p2 = expand(field, dim, 18)
    print(f"A2: {p2[-1]}")

if __name__ == '__main__':
    main()
