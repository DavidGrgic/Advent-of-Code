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
    data = ''
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            data += ln.replace('\n', '')

    # Part 1
    p2 = 0
    dat = copy.copy(data)
    # Canceled
    while (i := dat.find('!')) >= 0:
        dat = dat[:i] + dat[i+2:]
    # Garbage
    while (i := dat.find('<')) >= 0:
        assert (j := dat[i:].find('>')) >= 0
        dat = dat[:i] + dat[i+j+1:]
        p2 += j-1
    p1 = 0
    score = 1
    for d in dat:
        match d:
            case '{':
                p1 += score
                score += 1
            case '}':
                score -= 1
    print(f"A1: {p1}")

    # Part 2
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
