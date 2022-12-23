# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: '.', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img
img = lambda x: _img_print(_dict2img({i: 1 for i in x.values()}))

def main():
    # Read
    data = {}
    k = -1
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            for i, v in enumerate(ln):
                if v == '#':
                    k += 1
                    data.update({k: (c,i)})

    smer = {'N': (-1,0), 'NW': (-1,-1), 'W': (0,-1), 'SW': (1,-1), 'S': (1,0), 'SE': (1,1), 'E': (0,1), 'NE': (-1,1)}
    order = ['N', 'S', 'W', 'E']
    prev = {'N': {'N', 'NW', 'NE'}, 'W': {'W', 'NW', 'SW'}, 'S': {'S', 'SW', 'SE'}, 'E': {'E', 'SE', 'NE'}}
    plus = lambda x, y: (x[0]+y[0],x[1]+y[1])
    chk = lambda da, x, d: not any(plus(x, smer[j]) in da.values() for j in prev[d])
    
    def runda(dat, k):
        _o = order[(k % len(order)):] + order[:(k % len(order))]
        _dat = copy.deepcopy(dat)
        for e, p in dat.items():
            if any(plus(p, v) in dat.values() for j, v in smer.items()):
                for i in _o:
                    if chk(dat, p, i):
                        _dat[e] = plus(p, smer[i])
                        break
        uni = {k for k, v in Counter(_dat.values()).items() if v == 1}
        return {k: v if v in uni else dat[k] for k, v in _dat.items()}
        
    
    # Part 1
    if True:
        dat=copy.deepcopy(data)
        for k in range(10):
            dat = runda(dat, k)
            #print(k+1); img(dat)
        print(f"A1: {(_dict2img({i: 1 for i in dat.values()}) == 0).sum()}")

    # Part 2
    dat=copy.deepcopy(data)
    k = 0
    while True:
        dat_ = copy.deepcopy(dat)
        dat = runda(dat, k)
        k += 1
        if dat_ == dat:
            break
        #if k % 25 == 0: print(k, len(set(dat.values()) - set(dat_.values())))
    print(f"A2: {k}")

if __name__ == '__main__':
    main()
