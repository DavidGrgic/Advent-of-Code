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
    filename = 'd.txt'
    
    # Read
    data = []
    with open(filename, 'r') as file:
        for c, ln in enumerate(file):
            data.extend(int(i) for i in ln.replace('\n', '').split(','))
    # Part 1
    if True:
        numbers = np.array(range(256 if max(data) > 5 else 5))
        dim = numbers.shape[0]
        current = 0
        for skip, length in enumerate(data):
            idx = [i % dim for i in range(current, current+length)]
            numbers[idx] = numbers[idx][::-1]
            current = (current + length + skip) % dim
        print(f"A1: {int(numbers[:2].prod())}")

    # Part 2
    # Re-read
    data = []
    with open(filename, 'r') as file:
        for c, ln in enumerate(file):
            data.extend(ord(i) for i in ln.replace('\n', ''))
    data.extend([17, 31, 73, 47, 23])

    numbers = np.array(range(256 if max(data) > 5 else 5))
    dim = numbers.shape[0]
    current = skip = 0
    for _ in range(64):
        for length in data:
            idx = [i % dim for i in range(current, current+length)]
            numbers[idx] = numbers[idx][::-1]
            current = (current + length + skip) % dim
            skip += 1
    dense = []
    for i in range(0, dim, 16):
        num = 0
        for j in range(i, i+16):
            num ^= int(numbers[j])
        dense.append(num)
    p2 = ''.join(hex(i)[2:].rjust(2, '0') for i in dense)
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
