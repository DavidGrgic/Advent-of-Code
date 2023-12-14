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
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    okrogle = set()
    kvadratne = set()
    with open('t.txt', 'r') as file:
        for r, ln in enumerate(file):
            ln = ln.replace('\n', '')
            for c, v in enumerate(ln):
                if v == 'O':
                    okrogle |= {(r,c)}
                elif v == '#':
                    kvadratne |= {(r,c)}
                elif v != '.':
                    raise ValueError

    rows = max(i[0] for i in kvadratne | okrogle)
    cols = max(i[1] for i in kvadratne | okrogle)
    # Part 1
    if False:
        okr = copy.deepcopy(okrogle)
        for r in range(rows+1):
            vrsta = {i for i in okr if i[0] == r}
            for k in vrsta:
                nad = {i for i in kvadratne | okr if i[0] < k[0] and i[1] == k[1]}
                if len(nad) == 0:
                    rr = 0
                else:
                    rr = max(i[0] for i in nad) + 1
                okr = okr.difference({k}) | {(rr, k[1])}
        p1 = [rows - i[0] +1 for i in okr]
        print(f"A1: {sum(p1)}")

    # Part 2
    assert rows == cols
    nn = 1000000000
    nn = 1
    okr = copy.deepcopy(okrogle)
    cikel = [hash(tuple(sorted(okr)))]
    while True:
        for spin in [(0, -1), (1, 1), (0, 1), (1, -1)]:   # (dimenzija (0 gor dol, 1 levo desno), smer)
            
            
            for r in (range(rows+1) if spin[1] == -1 else range(rows+1, 0, -1)):
                vrsta = {i for i in okr if i[spin[0]] == r}
                for k in vrsta:
                    nad = {i for i in kvadratne | okr if i[0] < k[0] and i[1] == k[1]}
                    if len(nad) == 0:
                        rr = 0
                    else:
                        rr = max(i[0] for i in nad) + 1
                    okr = okr.difference({k}) | {(rr, k[1])}
            
        
        
        
        
        
        has = hash(tuple(sorted(okr)))
        if has in cikel:
            break
        else:
            cikel.append(has)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
