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
    data = []
    dat = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                data.append(np.array(dat, dtype = int))
                dat = []
                continue
            dat.append([1 if i == '#' else 0 for i in ln])
    data.append(np.array(dat, dtype = int))

    def prelom(polje):
        for i in range(1, polje.shape[0]):
            if (polje[max(0, 2*i - polje.shape[0]):i] == polje[i:i+i][::-1,:]).all():
                return i

    # Part 1
    if True:
        p1 = []
        for k, dat in enumerate(data):
            os = prelom(dat)
            if os is None:
                os = prelom(dat.T)
            else:
                os *= 100
            p1.append(os)
        print(f"A1: {sum(p1)}")

    # Part 2
    p2 = []
    for k, dat in enumerate(data):
        ok = False
        for i in range(dat.shape[0]):
            for j in range(dat.shape[1]):
                da = dat.copy()
                da[i,j] = 0 if da[i,j] else 1
                os = prelom(da)
                if os is None or os == prelom(dat):
                    os = prelom(da.T)
                    if os is None or os == prelom(dat.T):
                        continue
                else:
                    os *= 100
                ok = True
                break
            if ok:
                break
        p2.append(os)
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()
