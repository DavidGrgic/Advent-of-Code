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
def plot(data, mapper: dict = {0: '.', 1: '#'}, default: dict = {set: 1, dict: 0}):
    if isinstance(data, set):
        data = {k: default[set] for k in data}
    if isinstance(data, dict):
        offset = tuple(int(min(i[j] for i in data.keys())) for j in range(2))
        img = np.zeros(tuple(int(max(i[j] for i in data.keys())-offset[j])+1 for j in range(2))).astype(int) + default[dict]
        img[tuple(tuple(int(i[j]-offset[j]) for i in data.keys()) for j in range(2))] = list(data.values())
        data = img
    print('\n'+'\n'.join([''.join(mapper.get(i,'?') for i in j) for j in data]))

def main():
    # Read
    data = ''
    with open('d.txt', 'r') as file:
        for l, ln in enumerate(file):
            data += ln.replace('\n', '')

    #data = 'A(1x5)BC'
    #data = '(3x3)XYZ'
    #data = 'A(2x2)BCD(2x2)EFG'
    #data = '(6x1)(1x3)A'
    #data = 'X(8x2)(3x3)ABCY'
    #data = '(27x12)(20x12)(13x14)(7x10)(1x12)A'
    #data = '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'

    # Part 1
    if True:
        i = 0
        dat = ''
        while (i_ := data[i:].find('(')) >= 0:
            dat += data[i:i+i_]
            assert (_i := data[i + i_:].find(')')) > 0, "Wrong expansion instruction."
            l, m = [int(j) for j in data[i + i_ + 1: i + i_ + _i].split('x')]
            dat += m * data[i+i_+_i+1:(i := i+i_+_i+l+1)]
        dat += data[i:]
        print(f"A1: {len(dat)}")

    # Part 2
    def decomp(data: str):
        i = 0
        dat = ''
        while (i_ := data[i:].find('(')) >= 0:
            dat += data[i:i+i_]
            assert (_i := data[i + i_:].find(')')) > 0, "Wrong expansion instruction."
            l, m = [int(j) for j in data[i + i_ + 1: i + i_ + _i].split('x')]
            dat += decomp(m * data[i+i_+_i+1:(i := i+i_+_i+l+1)])
        dat += data[i:]
        return dat

    p2 = decomp(data)
    print(f"A2: {len(p2)}")

if __name__ == '__main__':
    main()
