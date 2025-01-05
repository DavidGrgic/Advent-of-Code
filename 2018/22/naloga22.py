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
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            match ln.replace('\n', '').split(': '):
                case 'depth', x:
                    depth = int(x)
                case 'target', x:
                    target = tuple(int(i) for i in x.split(','))
    # For second part, how much field should be extended for second part puzzle. Since switching a tool takes 7 minutes (moves), it sounds like 7 or slightly more is OK selection
    extend = 10

    eros = lambda v: (v+depth)%20183
    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])

    # Part 1
    geologic = {(x,0): 16807*x for x in range(target[0]+1+extend)} | {(0,y): 48271*y for y in range(target[1]+1+extend)} | {target: 0}
    erosion = {xy: eros(v) for xy,v in geologic.items()}
    for x in range(target[0]+1+extend):
        for y in range(target[1]+1+extend):
            if (x,y) not in geologic:
                geologic.update({(x,y): erosion[(x-1,y)]*erosion[(x,y-1)]})
                erosion.update({(x,y): eros(geologic[(x,y)])})
    region = {xy: v%3 for xy, v in erosion.items()}
    
    if True:
        print(f"A1: {sum(v for (x,y),v in region.items() if x <= target[0] and y <= target[1])}")

    # Part 2
    tool = {'t': {0, 2}, 'c': {0, 1}, 'n': {1, 2}}
    rob = [(xy+(k,), plus(xy,d)+(k,), 1) for k, v in tool.items() for xy, v_ in region.items() for d in {(1,0), (0,1)} if v_ in v and region.get(plus(xy,d)) in v]
    rob += [(xy+(k,), xy+(k_,), 7) for k, k_ in {('t','c'), ('t','n'), ('c','n')} for xy, v in region.items() if v in tool[k] and v in  tool[k_]]
    G = nx.Graph()
    G.add_weighted_edges_from(rob)
    pot = nx.shortest_path(G, (0,0,'t'), target + ('t',), 'weight')
    p2 = sum(1 if pot[i][-1] == pot[i+1][-1] else 7 for i in range(len(pot)-1))
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
