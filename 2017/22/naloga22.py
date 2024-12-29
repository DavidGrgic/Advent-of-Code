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
    infected = set()  # Infected nodes
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            for j, v in enumerate(ln.replace('\n', '')):
                if v == '#':
                    infected.add((i,j))
    position = (i//2, j//2)
    direction = (-1,0)
    
    left = {(-1,0):(0,-1), (0,-1):(1,0), (1,0):(0,1), (0,1):(-1,0)}
    right = {v:k for k, v in left.items()}
    reverse = lambda a: (-a[0], -a[1])
    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])
    
    # Part 1
    if True:
        inf = infected.copy()
        pos = copy.copy(position)
        di = copy.copy(direction)
        p1 = 0
        for _ in range(10**4):
            di = (right if pos in inf else left)[di]
            if pos in inf:
                inf -= {pos}
            else:
                inf |= {pos}
                p1 += 1
            pos = plus(pos, di)
        print(f"A1: {p1}")

    # Part 2
    inf = infected.copy()
    weak = set()
    flag = set()
    pos = copy.copy(position)
    di = copy.copy(direction)
    p2 = 0
    for _ in range(10**7):
        if pos in inf:
            di = right[di]
            inf.remove(pos)
            flag.add(pos)
        elif pos in weak:
            weak.remove(pos)
            inf.add(pos)
            p2 += 1
        elif pos in flag:
            di = reverse(di)
            flag.remove(pos)
        else:
            di = left[di]
            weak.add(pos)
        pos = plus(pos, di)
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
