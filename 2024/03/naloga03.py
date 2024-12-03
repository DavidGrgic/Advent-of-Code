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
    if True:
        p1 = []
        for da in data.split('mul(')[1:]:
            d = da.split(')')[0].split(',')
            if len(d) == 2 and all(i.isnumeric() for i in d):
                p1.append((int(d[0]), int(d[1])))
        print(f"A1: {sum(i[0]*i[1] for i in p1)}")

    # Part 2
    p2 = []
    enabled = True
    for idx, da in enumerate(data.split('mul(')):
        if idx != 0 and enabled:
            d = da.split(')')[0].split(',')
            if len(d) == 2 and all(i.isnumeric() for i in d):
                p2.append((int(d[0]), int(d[1])))
        ja = da[::-1].find(")(od")
        ne = da[::-1].find(")(t'nod")
        match ja >= 0, ne >= 0:
            case (True, True):
                enabled = ja < ne
            case (True, False):
                enabled = True
            case (False, True):
                enabled = False
    print(f"A2: {sum(i[0]*i[1] for i in p2)}")

if __name__ == '__main__':
    main()
