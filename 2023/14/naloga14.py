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
_img_map = {0: '.', 1: 'O', 2: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _sets2img(y, z):
    x = {i: 1 for i in y} | {i: 2 for i in z}
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    okrogle = set()
    kvadratne = set()
    with open('d.txt', 'r') as file:
        for r, ln in enumerate(file):
            ln = ln.replace('\n', '')
            for c, v in enumerate(ln):
                if v == 'O':
                    okrogle |= {(r,c)}
                elif v == '#':
                    kvadratne |= {(r,c)}
                elif v != '.':
                    raise ValueError

    size = max(i[0] for i in kvadratne | okrogle)
    # Part 1
    if True:
        okr = copy.deepcopy(okrogle)
        for r in range(size+1):
            vrsta = {i for i in okr if i[0] == r}
            for k in vrsta:
                nad = {i for i in kvadratne | okr if i[0] < k[0] and i[1] == k[1]}
                if len(nad) == 0:
                    rr = 0
                else:
                    rr = max(i[0] for i in nad) + 1
                okr = okr.difference({k}) | {(rr, k[1])}
        p1 = [size - i[0] +1 for i in okr]
        print(f"A1: {sum(p1)}")

    # Part 2
    assert size == max(i[1] for i in kvadratne | okrogle)
    nn = 1000000000
    okr = copy.deepcopy(okrogle)
    cikel = [hash(tuple(sorted(okr)))]
    resitev = [okr]
    while True:
        for spin in [(0, -1), (1, -1), (0, 1), (1, 1)]:   # (axis, direction)
            for r in (range(size+1) if spin[1] == -1 else range(size, -1, -1)):
                vrsta = {i for i in okr if i[spin[0]] == r}
                for k in vrsta:
                    nad = {i for i in kvadratne | okr if spin[1] * i[spin[0]] > spin[1] * k[spin[0]] and i[(spin[0] + 1 ) % 2] == k[(spin[0] + 1 ) % 2]}
                    if len(nad) == 0:
                        rr = 0 if spin[1] == -1 else size
                    else:
                        rr = max(i[spin[0]] for i in nad) + 1 if spin[1] == -1 else min(i[spin[0]] for i in nad) - 1
                    okr = okr.difference({k}) | {(rr, k[1]) if spin[0] == 0 else (k[0], rr)}
        #_img_print(_sets2img(okr, kvadratne))
        has = hash(tuple(sorted(okr)))
        if has in cikel:
            break
        else:
            cikel.append(has)
            resitev.append(okr)
    offset = cikel.index(has)
    perioda = len(cikel) - offset
    zadnji = resitev[offset + ((nn - offset) % perioda)]
    p2 = [size - i[0] +1 for i in zadnji]
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()
