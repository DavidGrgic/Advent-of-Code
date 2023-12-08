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
    lr = []
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if len(lr) == 0:
                lr = ln
                continue
            if ln == '': # Nov blok podatkov
                continue
            da = ln.split(' = ')
            data.update({da[0]: tuple(da[1][1:-1].split(', '))})

    def dolzina(tocka, end):
        k = 0
        while tocka[-len(end):] != end:
            tocka = data[tocka][0 if lr[k % len(lr)] == 'L' else 1]
            k += 1
        return k

    # Part 1
    if True:
        k = 0
        tocka = 'AAA'
        while tocka != 'ZZZ':
            idx = lr[k % len(lr)]
            tocka = data[tocka][0 if idx == 'L' else 1]
            k += 1
        p1 = dolzina('AAA', 'ZZZ')
        print(f"A1: {p1}")

    # Part 2
    starts = [i for i in data.keys() if i[-1] == 'A']
    p2 = []
    for i in starts:
        p2.append(dolzina(i, 'Z'))
    print(f"A2: {math.lcm(*tuple(p2))}")

if __name__ == '__main__':
    main()
