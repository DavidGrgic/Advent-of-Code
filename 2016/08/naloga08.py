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
def plot(data, mapper: dict = {0: ' ', 1: '#'}, default: dict = {set: 1, dict: 0}):
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
            match ln.replace('\n', '').split():
                case 'rect', d:
                    data.append(('rec',) + tuple(int(i) for i in d.split('x')))
                case 'rotate', 'row', y, 'by', v:
                    data.append(('row', int(y.split('=')[-1]), int(v)))
                case 'rotate', 'column', x, 'by', v:
                    data.append(('col', int(x.split('=')[-1]), int(v)))
                case _:
                    raise Exception('Unknown input.')
                    
    YX = (50,6) if len(data) > 5 else (7,3)

    # Part 1
    if True:
        screen = set()
        for ins in data:
            match ins:
                case 'rec', w, t:
                    screen |= {(y,x) for x in range(w) for y in range(t)}
                case 'row', y, v:
                    screen = {(j, (i + v) % YX[0]) if j == y else (j, i)  for j,i in screen}
                case 'col', x, v:
                    screen = {((j + v) % YX[1], i) if i == x else (j, i)  for j,i in screen}
                case _:
                    raise Exception('Unknown instruction.')
        print(f"A1: {len(screen)}")

    # Part 2
    print("A2:", end = '')
    plot(screen)

if __name__ == '__main__':
    main()
