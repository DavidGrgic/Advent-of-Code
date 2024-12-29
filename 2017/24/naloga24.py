# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
from functools import cache   # @cache
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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            data.append(tuple(int(i) for i in  ln.replace('\n', '').split('/')))

    @cache
    def bridge(parts, end = 0, long = False, strong = True):
        fit = {i for i in parts if end in i}
        ret = [()]
        for fi in fit:
            idx = parts.index(fi)
            bri = bridge(parts[:idx] + parts[idx+1:], (fi[:(i:=fi.index(end))] + fi[i+1:])[0], long, strong)
            ret += [(fi,) + b for b in bri]
        if long:
            ll = max(len(b) for b in ret)
            ret = [b for b in ret if len(b) == ll]
        ret = sorted(ret, key = lambda b: sum(j for i in b for j in i), reverse = True)
        if strong:  # Return only strongest
            ret = ret[:1]
        return ret
    
    # Part 1
    if True:
        p1 = bridge(tuple(data))
        print(f"A1: {sum(j for i in p1[0] for j in i)}")

    # Part 2
    p2 = bridge(tuple(data), long = True)
    print(f"A2: {sum(j for i in p2[0] for j in i)}")

if __name__ == '__main__':
    main()
