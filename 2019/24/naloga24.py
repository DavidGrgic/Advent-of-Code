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
    data = set()
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data |= {(c, i) for i, v in enumerate(ln) if v == '#'}
    dim = c+1
    assert dim == len(ln)

    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])
    def okolica(ij, da):
        return sum(plus(ij, s) in dat for s in {(-1,0), (1,0), (0,-1), (0,1)})

    # Part 1
    if True:
        prostor = {(i, j) for i in range(dim) for j in range(dim)}
        p1 = []
        dat=copy.deepcopy(data)
        while dat not in p1[:-1]:
            dat_ = set()
            for ij in dat:
                if okolica(ij, dat) == 1:
                    dat_ |= {ij}
            for ij in prostor - dat:
                if 1 <= okolica(ij, dat) <= 2:
                    dat_ |= {ij}
            p1.append(dat_)
            dat = dat_
        print(f"A1: {sum(2 ** (i[0]*dim + i[1]) for i in dat)}")

    # Part 2
    minut = 200
    port = dim // 2
    sosedje = [((i,j), (plus((i,j),s),0)) for i in range(dim) for j in range(dim) for s in {(-1,0), (1,0), (0,-1), (0,1)} if (i,j) != 2*(port,)]
    sosedje = [(ij,((port-1,port),d-1)) if x < 0 else (ij,((x,y),d)) for (ij,((x,y),d)) in sosedje]
    sosedje = [(ij,((port+1,port),d-1)) if x >= dim else (ij,((x,y),d)) for (ij,((x,y),d)) in sosedje]
    sosedje = [(ij,((port,port-1),d-1)) if y < 0 else (ij,((x,y),d)) for (ij,((x,y),d)) in sosedje]
    sosedje = [(ij,((port,port+1),d-1)) if y >= dim else (ij,((x,y),d)) for (ij,((x,y),d)) in sosedje]
    sosedje = [(ij,(xy,d)) for (ij,(xy,d)) in sosedje if xy != 2*(port,)] + \
        [((port-1,port), ((0,j),1)) for j in range(dim)] + \
        [((port,port-1), ((i,0),1)) for i in range(dim)] + \
        [((port,port+1), ((i,dim-1),1)) for i in range(dim)] + \
        [((port+1,port), ((dim-1,j),1)) for j in range(dim)]
    sosedje = {ij: [xyd for (ij_, xyd) in sosedje if ij_ == ij] for (ij,_) in sosedje}
    dat = {ij + (0,) for ij in data}
    for mi in range(1, minut+1):
        dat_ = set()
        for ijl in {(i, j, l) for i in range(dim) for j in range(dim) if (i,j) != (port,port) for l in range(-mi, mi+1)}:
            okoli = sum(xy+(ijl[-1]+d,) in dat for xy, d in sosedje[ijl[:2]])
            if (ijl in dat and okoli == 1) or (ijl not in dat and 1 <= okoli <= 2):
                dat_ |= {ijl}
        dat = dat_
    print(f"A2: {len(dat)}")

if __name__ == '__main__':
    main()
