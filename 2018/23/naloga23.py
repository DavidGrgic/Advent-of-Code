# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from fractions import Fraction
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
    data = []
    with open('t2.txt', 'r') as file:
        for c, ln in enumerate(file):
            da = ln.replace('\n', '').split('>, r=')
            data.append((tuple(int(i) for i in da[0][5:].split(',')), int(da[1])))
    assert len(data) == len(data := set(data)), "Code is optimised to work with set... if nanorobots are duplicated by position and radius, code should be updated"

    distance = lambda a, b = (0,0,0): sum(abs(i-j) for i,j in zip(a,b))

    def explore(candidates, intersect = None, included = None):
        if len(candidates) == 0:
            return -len(included), max(0, distance(intersect[0]) - intersect[-1])
        ret = set()
        done = set()
        for nanobot in candidates:
            done.add(nanobot)
            if intersect is None:
                included = set()
                sub_intersect = nanobot
            else:
                rang = Fraction(intersect[1] + nanobot[1] - distance(intersect[0], nanobot[0]), 2)
                if rang < 0:
                    continue
                rr = Fraction(intersect[1], intersect[1] + nanobot[1])
                sub_intersect = tuple(i+rr*(j-i) for i,j in zip(intersect[0], nanobot[0])), rang
            ret_ = explore(candidates - done, sub_intersect, included | {nanobot})
            ret.add(ret_)
#        if len(ret) == 0:
#            return -len(included), max(0, distance(intersect[0]) - intersect[-1])
        return sorted(ret)[0]

    # Part 1
    if True:
        strongest = [k for k in sorted(data, key=lambda i: i[-1], reverse=True)][0]
        p1 = [k for k in data if distance(strongest[0], k[0]) <= strongest[-1]]
        print(f"A1: {len(p1)}")

    # Part 2
    p2 = explore(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
