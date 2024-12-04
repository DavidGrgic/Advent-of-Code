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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += [[i for i in ln]]
    data = np.array(data)
    assert len(set(data.shape)) == 1

    def stej(line):
        no = 0
        ln = ''.join(j for j in line)
        l = ln
        for l in (ln, ln[::-1]):
            while len(l) > 3:
                idx = l.find('XMAS')
                if idx == -1:
                    break
                else:
                    no += 1
                    l = l[idx+1:]
        return no

    # Part 1
    dim = data.shape[0]
    if True:
        p1 = 0
        for dat in (data, data.T):
            for l in dat:
                p1 += stej(l)
        for dat in (data, data[::-1]):
            for i in range(-dim+1, dim-1):
                l = np.diag(dat, i)
                p1 += stej(l)
        print(f"A1: {p1}")

    # Part 2
    p2 = 0
    for i in range(1, dim-1):
        for j in range(1, dim-1):
            if data[i, j] == 'A':
                x = ''.join(data[i+x, j+y] for x,y in [(-1, -1), (-1, 1), (1, 1), (1, -1)])
                if x in {'MSSM', 'SSMM', 'SMMS', 'MMSS'}:
                    p2 += 1
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
