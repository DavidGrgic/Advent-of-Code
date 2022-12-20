# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
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
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            data += [int(ln.replace('\n', ''))]

    def after(dat, ite, num = 0):
        for i in range(ite):
            num = dat[num]
        return num

    # Part 1
    if True:
        dat = {i: i+1 if i+1 < len(data) else 0 for i in range(len(data))}
        for i in data:
            if i == 0 or abs(i) in {len(dat),len(dat)-1}:
                continue
            inv = {v: k for k, v in dat.items()}
            nxt = _nxt = dat[data.index(i)]
            pre = _pre = inv[data.index(i)]
            dat[_pre] = _nxt
            del dat[data.index(i)]
            for _ in range(abs(i) + abs(i) // len(dat)):
                if i > 0:
                    pre = nxt
                    nxt = dat[nxt]
                else:
                    nxt = pre
                    pre = inv[pre]
            dat[pre] = data.index(i)
            dat[data.index(i)] = nxt
   #         dat[_pre] = _nxt

        print(f"A1: {sum(data[after(dat, i * 1000, data.index(0))] for i in range(1,4))}")
        # 7407 is too low
        # 20985 is to high

    # Part 2
    dat=copy.deepcopy(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
