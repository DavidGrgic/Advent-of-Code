# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
import datetime as dt
from collections import Counter
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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            d, e = ln.replace('\n', '')[1:].split('] ')
            data.append((dt.datetime.strptime(d, '%Y-%m-%d %H:%M'), e))
    data = sorted(data)
    dat = {}
    for i in data:
        match i:
            case t, 'falls asleep':
                assert dt.time(0,0) <= t.time() <= dt.time(0,59), f"Wrong asleep time: {t}"
                sleep = t
            case t, 'wakes up':
                assert dt.time(0,0) <= t.time() <= dt.time(0,59), f"Wrong weaks time: {t}"
                assert t-sleep <= dt.timedelta(minutes = 59), "To long sleep."
                dat.update({guard: dat.get(guard, []) + [{i for i in range(sleep.minute, t.minute)}]})
            case t, v:
                guard = int(v.split()[1][1:])

    # Part 1
    if True:
        p1 = {k: sum(len(i) for i in v) for k,v in dat.items()}
        guard = sorted(p1.items(), key=lambda i: i[1], reverse=True)[0][0]
        p1 = Counter(j for i in dat[guard] for j in i)
        minute = sorted(p1.items(), key=lambda i: i[1], reverse=True)[0][0]
        print(f"A1: {guard*minute}")

    # Part 2
    p2 = {g: sorted(Counter(j for i in v for j in i).items(), key=lambda i: i[1], reverse=True)[0] for g, v in dat.items()}
    guard, (minute, _) = sorted(p2.items(), key=lambda i: i[1][1], reverse=True)[0]
    print(f"A2: {guard*minute}")

if __name__ == '__main__':
    main()
