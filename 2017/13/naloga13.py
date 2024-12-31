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
            da = ln.replace('\n', '').split(':')
            data.update({int(da[0]): int(da[-1])})

    # Part 1
    if True:
        # Sensor is moving with frequency 2 * (range - 1), torej je na vrhu ob vsakih 2*(t-1)
        # Packeth se gibleje linarno, torej je na vrh vsakega layerja ob času enak depth, torej ob t
        # Torej se packet in sensor srečata, ko je ostanek daljenja depth % (2 * (range-1)) enak 0
        p1 = {d: r for d, r in data.items() if d % (2 * (r - 1)) == 0}
        print(f"A1: {sum(d*r for d, r in p1.items())}")

    # Part 2
    t = 0
    while len([d for d, r in data.items() if (t+d) % (2 * (r - 1)) == 0]) > 0:
        t += 1
    print(f"A2: {t}")

if __name__ == '__main__':
    main()
