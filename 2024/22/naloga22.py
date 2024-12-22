# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product
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
            data += [int(ln)]

    def secret(num, nn = 2000):
        final = lambda x: (x ^ num) % 16777216
        for _ in range(nn):
            num = final(num * 64)
            num = final(num // 32)
            num = final(num * 2048)
        return num

    def change(num, nn = 2000):
        final = lambda x: (x ^ num) % 16777216
        prices = [num % 10]
        for _ in range(nn):
            num = final(num * 64)
            num = final(num // 32)
            num = final(num * 2048)
            prices.append(num % 10)
        changes = tuple(prices[i+1]-prices[i] for i in range(len(prices)-1))
        return prices, changes

    # Part 1
    if True:
        p1 = []
        for dat in data:
            p1.append(secret(dat))
        print(f"A1: {sum(p1)}")

    # Part 2
    find = lambda x, s: [(i, i+len(s)) for i in range(len(x)-len(s)+1) if x[i:i+len(s)] == s]
    first = lambda x: [x[0]] if len(x) > 0 else []
    prices = []
    changes = []
    for dat in data:
        p, c = change(dat)
        prices.append(p)
        changes.append(c)
    sequences = [i for i in product(*(range(-9,10),)*4) if 0 < sum(i) < 10]  # Only make sanse if sum is above 0 and equal or below 9
    best = 0
    for seq in sorted(sequences, key = lambda x: sum(x)):  # Higher chanses have sequences with smallest sum
        if (best_ := sum(prices[i][f[-1]] for i, chng in enumerate(changes) for f in first(find(chng, seq)))) > best:
            best = best_
            if True:
                print(seq, best)
    print(f"A2: {best}")

if __name__ == '__main__':
    main()
