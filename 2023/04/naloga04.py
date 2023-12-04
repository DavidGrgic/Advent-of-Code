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
            d = da[1].split('|')
            w = [int(i) for i in d[0].split()]
            n = [int(i) for i in d[1].split()]
            data.update({c: (w, n)})

    # Part 1
    win = {}
    if True:
        for k, v in data.items():
            w = []
            for i in v[1]:
                if i in v[0]:
                    w.append(i)
            win.update({k: w})
        win = [len(i) for i in win.values()]
        print(f"A1: {sum(i if i <= 1 else 2**(i-1) for i in win)}")

    # Part 2
    dat = [1] * len(data)
    for k in range(len(dat)):
        for i in range(win[k]):
            if k+i+1 < len(dat):
                dat[k+i+1] += dat[k]
    print(f"A2: {sum(dat)}")

if __name__ == '__main__':
    main()
