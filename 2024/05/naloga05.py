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
    order = []
    upp = []
    update = False
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                update = True
                continue
            if update:
                da = ln.split(',')
                upp.append([int(i) for i in da])
            else:
                da = ln.split('|')
                order.append((int(da[0]), int(da[1])))

    def check(x, y):
        for oo in order:
            if x == oo[1] and y == oo[0]:
                return False
        return True

    # Part 1
    if True:
        p1ok = []
        for up in upp:
            ok = True
            for i, u in enumerate(up[:-1]):
                ok = ok and check(u, up[i+1])
                if not ok:
                    continue
            if ok:
                p1ok.append(up)
        p1 = [i[len(i) // 2] for i in p1ok]
        print(f"A1: {sum(p1)}")

    # Part 2
    p2ok = []
    for up in [i for i in upp if i not in p1ok]:
        new = copy.copy(up)
        i = 0
        while i < (len(new) - 1):
            if check(new[i], new[i+1]):
                i += 1
            else:
                new[i], new[i+1] = new[i+1], new[i]
                i = max(0, i - 1)
        p2ok.append(new)
    p2 = [i[len(i) // 2] for i in p2ok]
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()
