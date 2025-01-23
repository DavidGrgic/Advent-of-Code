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
            match ln.replace('\n', '').split():
                case 'swap', 'position', x, 'with', 'position', y:
                    data.append(('swp', int(x), int(y)))
                case 'swap', 'letter', x, 'with', 'letter', y:
                    data.append(('swl', x, y))
                case 'rotate', d, x, 'steps' | 'step':
                    data.append(('rot', (1 if d == 'left' else -1) * int(x)))
                case 'rotate', 'based', 'on', 'position', 'of', 'letter', x:
                    data.append(('rop', x))
                case 'reverse', 'positions', x, 'through', y:
                    data.append(('rev', int(x), int(y)))
                case 'move', 'position', x, 'to', 'position', y:
                    data.append(('mov', int(x), int(y)))
                case _:
                    raise Exception('Unrecognized command.')

    def scramble(command: tuple, password: list[str]):
        pwd = list(password)
        match command:
            case 'swp', x, y:
                pwd[x], pwd[y] = pwd[y], pwd[x]
            case 'swl', a, b:
                x = pwd.index(a)
                y = pwd.index(b)
                pwd[x], pwd[y] = pwd[y], pwd[x]
            case 'rot', n:
                pwd = pwd[n:] + pwd[:n]
            case 'rop', a:
                n = (i := pwd.index(a)) + 1
                n = (n + (i >= 4)) % len(pwd)
                pwd = pwd[-n:] + pwd[:-n]
            case 'rev', x, y:
                pwd = pwd[:x] + pwd[x:y+1][::-1] + pwd[y+1:]
            case 'mov', x, y:
                a = pwd.pop(x)
                pwd.insert(y, a)
        return ''.join(pwd)

    # Part 1
    if True:
        password = 'abcdefgh' if len(data) > 10 else 'abcde'
        for dat in data:
            password = scramble(dat, password)
        print(f"A1: {password}")

    # Part 2
    scr_password = 'fbgdceah'
    for scr in permutations(scr_password):
        password = (un_password := ''.join(scr))
        for dat in data:
            password = scramble(dat, password)
        if password == scr_password:
            break
    print(f"A2: {un_password}")

if __name__ == '__main__':
    main()
