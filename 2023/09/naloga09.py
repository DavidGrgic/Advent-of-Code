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
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [int(i) for i in ln.split()]
            data += [da]

    # Part 1
    if True:
        dat=copy.deepcopy(data)
        for da in dat:
            seq = [da]
            while not all(i == 0 for i in seq[-1]):
                seq.append([seq[-1][i+1] - seq[-1][i] for i in range(len(seq[-1])-1)])
            for i in range(len(seq)-1,-1,-1):
                if i == len(seq) -1:
                    seq[i].append(seq[i][-1])
                else:
                    seq[i].append(seq[i][-1] + seq[i+1][-1])
        print(f"A1: {sum([i[-1] for i in dat])}")

    # Part 2
    dat=copy.deepcopy(data)
    for da in dat:
        seq = [da]
        while not all(i == 0 for i in seq[-1]):
            seq.append([seq[-1][i+1] - seq[-1][i] for i in range(len(seq[-1])-1)])
        for i in range(len(seq)-1,-1,-1):
            if i == len(seq) -1:
                seq[i].insert(0, seq[i][0])
            else:
                seq[i].insert(0, seq[i][0] - seq[i+1][0])
    print(f"A2: {sum([i[0] for i in dat])}")

if __name__ == '__main__':
    main()
