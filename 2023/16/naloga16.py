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
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: '.', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
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
            ln = ln.replace('\n', '')
            data += [ln]

    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])
    val = lambda x, y: data[x][y]
    size = len(data)
    assert size == len(data[0])

    def nxt(tocka, smer):
        smeri = set()
        if val(*tocka) == '.':
            smeri = {smer}
        elif val(*tocka) == '/':
            smeri = {(-smer[1], -smer[0])}
        elif val(*tocka) == '\\':
            smeri = {(smer[1], smer[0])}
        elif val(*tocka) == '-':
            smeri = {smer} if smer[1] != 0 else {(0,1), (0,-1)}
        elif val(*tocka) == '|':
            smeri = {smer} if smer[0] != 0 else {(1,0), (-1,0)}
        else:
            raise AssertionError
        tocke = set()
        for i in smeri:
            tocka_ = plus(tocka, i)
            plus(tocka, i)
            if 0 <= tocka_[0] < size and 0 <= tocka_[1] < size:
                tocke |= {(tocka_, i)}
        return tocke

    def sveti(tocka, smer):
        ll = 0
        zem = {(tocka, smer)}
        while ll != len(zem):
            ll = len(zem)
            zem |= {t for ts in zem for t in polje[ts]}
        return {i[0] for i in zem}

    polje = {((i, j), s): nxt((i, j), s)for i in range(size) for j in range(size) for s in {(1,0), (-1,0), (0,1), (0,-1)}}

    # Part 1
    if True:
        p1 = sveti((0,0), (0,1))
        #_img_print(_dict2img({i:1 for i in p1}))
        print(f"A1: {len(p1)}")

    # Part 2
    start = [((i,0), (0,1)) for i in range(size)]
    start += [((i,size-1), (0,-1)) for i in range(size)]
    start += [((0,i), (1,0)) for i in range(size)]
    start += [((size-1,i), (-1,0)) for i in range(size)]
    p2 = {}
    for sta in start:
        p2.update({sta: sveti(*sta)})
    print(f"A2: {max(len(i) for i in p2.values())}")

if __name__ == '__main__':
    main()
