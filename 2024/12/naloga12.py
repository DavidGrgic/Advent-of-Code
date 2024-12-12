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
            ln = ln.replace('\n', '')
            data.update({(c,i): v for i, v in enumerate(ln)})
    plus = lambda x, y: (x[0]+y[0], x[1]+y[1])

    def area(ij, area_ = None):
        if area_ is None:
            area_ = set((ij,))
        for s in {(1,0), (-1,0), (0,-1), (0,1)}:
            sosed = plus(ij, s)
            if data.get(sosed) == data[ij] and sosed not in area_:
                area_ |= {sosed}
                area(sosed, area_)
        return area_

    areas = []
    while len(nxt := set(data) - set(j for i in areas for j in i)) > 0:
        ij = next(iter(nxt))
        ar = area(ij)
        areas.append(ar)

    # Part 1
    if True:

        def fance(ar):
            ret = 0
            for ij in ar:
                for s in {(1,0), (-1,0), (0,-1), (0,1)}:
                    if plus(ij, s) not in ar:
                        ret += 1
            return ret

        p1 = 0
        for ar in areas:
            p1 += len(ar) * fance(ar)
        print(f"A1: {p1}")

    # Part 2
    def side(ar):
        ret = 0
        for s in {(1,0), (-1,0), (0,-1), (0,1)}:
            sosedi = {plus(ij,s) for ij in ar} - ar
            for ij_ in sosedi:
                if plus(ij_, s[::-1]) not in sosedi:
                    ret += 1
        return ret

    p2 = 0
    for ar in areas:
        p2 += len(ar) * side(ar)
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
