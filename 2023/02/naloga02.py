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
            da = ln.split(': ')
            k = int(da[0].replace('Game ', ''))
            da = da[1].split('; ')
            data.update({k: [{j.split()[-1]: int(j.split()[0]) for j in i.split(', ')} for i in da]})

    # Part 1
    if True:
        limit = {'red': 12, 'green': 13, 'blue': 14}
        possible = set()
        for k, v in data.items():
            ok = True
            for s in v:
                for c, n in limit.items():
                    if s.get(c, 0) > n:
                        ok = False
            if ok:
                possible |= {k}
        print(f"A1: {sum(possible)}")

    # Part 2
    games = []
    for k, v in data.items():
        mm = {i: 0 for i in limit}
        for c in limit:
            n = max(mm[c], max(j.get(c, 0) for j in v))
            mm[c] = n
        games.append(math.prod(mm.values()))
    print(f"A2: {sum(games)}")

if __name__ == '__main__':
    main()
