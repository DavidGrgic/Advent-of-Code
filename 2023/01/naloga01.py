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
            # da = [i for i in ln]
            # data += [da]
            data += [ln]

    # Part 1
    if False:
        p1 = []
        for row in data:
            p = []
            for col in row:
                if col.isdigit():
                    p += [col]
                    break
            for col in row[::-1]:
                if col.isdigit():
                    p += [col]
                    break
            p1 += [int(''.join(p))]
        print(f"A1: {sum(p1)}")

    def repl(row, last = False):
        res = []
        if last:
            row = row[::-1]
        for k, v in rep.items():
            res += [row.replace(k, str(v))]
        if last:
            res = [r[::-1] for r in res]
        res = sorted(res, key = lambda x: ''.join([str(1 if i.isdigit() else 0) for i in x]).find('1') if '1' in ''.join([str(1 if i.isdigit() else 0) for i in x]) else 10**5)[0]
        return res

    # Part 2
    rep = {'one': 1,'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}
    p1 = []
    for row in data:
        # for k, v in rep.items():
        #     row = row.replace(k, str(v))
        p = []
        rrr = repl(row)
        for col in rrr:
            if col.isdigit():
                p += [col]
                break
        rrr = repl(row[::-1], True)
        for col in rrr:
            if col.isdigit():
                p += [col]
                break
        p1 += [int(''.join(p))]
    print(f"A1: {sum(p1)}")

if __name__ == '__main__':
    main()
