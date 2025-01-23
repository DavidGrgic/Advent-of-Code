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


class Comp:
    
    def __init__(self, code):
        self.register = {chr(ord('a')+i): 0 for i in range(4)}
        self.code = code.copy() if isinstance(code, dict) else {i: v for i, v in enumerate(code)}
        self.pointer = 0
        self.output = []
        
    def run(self, output_halt = True):
        output = False
        while output_halt and not output:
            if (code := self.code.get(self.pointer)) is None:
                break
            match code:
                case 'cpy', x, y:
                    if isinstance(y, str):
                        self.register[y] = self.register[x] if isinstance(x, str) else x
                case 'inc', x:
                    self.register[x] += 1
                case 'dec', x:
                    self.register[x] -= 1
                case 'jnz', x, y:
                    if (self.register[x] if isinstance(x, str) else x):
                        self.pointer += (self.register[y] if isinstance(y, str) else y) - 1
                case 'tgl', x:
                    i = self.pointer + (self.register[x] if isinstance(x, str) else x)
                    if (code_ := self.code.get(i)) is not None:
                        match code_:
                            case c, x:
                                new = ({'inc': 'dec'}.get(c, 'inc'), x)
                            case c, x, y:
                                new = ({'jnz': 'cpy'}.get(c, 'jnz'), x, y)
                        self.code[i] = new
                case 'out', x:
                    self.output.append(self.register[x] if isinstance(x, str) else x)
                    output = True
                case _:
                    raise RuntimeError("fUnknown command '{_}'.")
            self.pointer += 1


def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            ins, *arg = ln.replace('\n', '').split()
            data.append((ins,) + tuple(int(i) if i.replace('-','').isnumeric() else i for i in arg))

    # Part 1
    n = 0
    while True:
        comp = Comp(data)
        comp.register['a'] = n
        state = []
        while True:
            comp.run()
            state.append(stat := tuple(i[1] for i in comp.register.items()) + tuple(i[1] for i in comp.code.items()))
            if len(comp) >= 2:
                pass
        
    print(f"A1: {n}")

if __name__ == '__main__':
    main()
