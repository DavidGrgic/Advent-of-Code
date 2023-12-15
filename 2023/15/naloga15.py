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
            data = ln.split(',')

    def has(data):
        value = 0
        for i in data:
            value += ord(i)
            value *= 17
            value %= 256
        return value

    # Part 1
    if True:
        p1 = [has(i) for i in data]
        print(f"A1: {sum(p1)}")

    # Part 2
    boxes = {i: [] for i in range(256)}
    for value in data:
        if value.endswith('-'):
            lab = value[:-1]
            box = has(lab)
            boxes[box] = [v for v in boxes[box] if v[0] != lab]
        else:
            enako = value.split('=')
            if len(enako) != 2:
                AssertionError
            lab = enako[0]
            box = has(lab)
            lens = int(enako[1])
            idx = [i for i, v in enumerate(boxes[box]) if v[0] == lab]
            if len(idx) == 0:
                boxes[box].append((enako[0], lens))
            else:
                boxes[box][next(iter(idx))] = (enako[0], lens)
    p2 = [(k+1) * (i+1) * j[1] for k, v in boxes.items() for i, j in enumerate(v)]
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()
