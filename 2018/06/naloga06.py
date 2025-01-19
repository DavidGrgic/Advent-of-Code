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
    data = set()
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            data.add(tuple(int(i) for i in ln.replace('\n', '').split(',')))

    distance = lambda a, b: sum(abs(i-j) for i,j in zip(a,b))
    xX_yY = [(min(i[j] for i in data), max(i[j] for i in data)) for j in range(2)]
    
    # Part 1
    if True:
        area = {k: 0 for k in data}
        infinite = set()
        for x in range(xX_yY[0][0], xX_yY[0][1] + 1):
            for y in range(xX_yY[1][0], xX_yY[1][1] + 1):
                dist = sorted({xy: distance((x,y), xy) for xy in data}.items(), key=lambda item: item[1])
                if dist[0][1] < dist[1][1]:
                    area[dist[0][0]] += 1
                    if x in xX_yY[0] or y in xX_yY[1]:
                        infinite.add(dist[0][0])
        area = {k: v for k, v in area.items() if k not in infinite}
        print(f"A1: {max(area.values())}")

    # Part 2
    total = 10000 if len(data) > 8 else 32
    over = total // len(data)
    p2 = 0
    for x in range(xX_yY[0][0] - over, xX_yY[0][1] + over + 1):
        for y in range(xX_yY[1][0] - over, xX_yY[1][1] + over + 1):
            dist = sum(distance((x,y), xy) for xy in data)
            if dist < total:
                p2 += 1
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
