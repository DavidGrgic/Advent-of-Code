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
    bias = 10000000000000
    data = []; da = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln.startswith('Button A: '):
                da.update({k: int(v) for k, v in zip(('Ax', 'Ay'), ln.lstrip('Button A: X').split(', Y'))})
            elif ln.startswith('Button B: '):
                da.update({k: int(v) for k, v in zip(('Bx', 'By'), ln.lstrip('Button B: X').split(', Y'))})
            elif ln.startswith('Prize: X='):
                da.update({k: int(v) for k, v in zip(('X', 'Y'), ln.lstrip('Prize: X=').split(', Y='))})
            elif ln == '':
                data += [da]
                da = {}
            else:
                raise
    data += [da]

    def opt(Ax, Ay, Bx, By, X, Y):
        ste = Y*Bx-X*By
        ime = Ay*Bx-Ax*By
        a, mod = divmod(ste, ime)
        if mod == 0:
            return a, (X - a * Ax) // Bx

    def optim(dat):
        cost = 0
        for d in dat:
            sol = opt(**d)
            if sol is not None:
                cost += 3*sol[0]+sol[1]
        return cost
    


    # Part 1
    if True:
        p1 = optim(data)
        print(f"A1: {p1}")

    # Part 2
    bias = 10000000000000
    p2 = optim([{k: v + (bias if k in {'X', 'Y'} else 0)for k, v in d.items()} for d in data])
    print(f"A2: {p2}")
    # fail: 68785870335896

if __name__ == '__main__':
    main()
