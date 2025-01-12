# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
from dataclasses import dataclass, field
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product, chain
#from functools import cache   # @cache
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

@dataclass
class Comp:
    code: list[tuple]
    register: list = field(default_factory=lambda: [0 for k in range(6)])
    bound: int = None

    def __post_init__(self):
        if self.code[0][0] == '#ip':
            self.bound =  self.code[0][1]
            self.code = self.code[1:]
        self.code = {i: v for i, v in enumerate(self.code)}

    def run(self, pointer: int = 0):
        while pointer in self.code:
            self.register[self.bound] = pointer
            step = self.code[pointer]
            #print(pointer, self.register, step, end=' ')
            getattr(self, step[0])(*step[1:])
            #print(self.register)
            pointer = self.register[self.bound]
            pointer += 1

    def addr(self, a, b, c):
        self.register[c] = self.register[a] + self.register[b]

    def addi(self, a, b, c):
        self.register[c] = self.register[a] + b

    def mulr(self, a, b, c):
        self.register[c] = self.register[a] * self.register[b]

    def muli(self, a, b, c):
        self.register[c] = self.register[a] * b

    def banr(self, a, b, c):
        self.register[c] = self.register[a] & self.register[b]

    def bani(self, a, b, c):
        self.register[c] = self.register[a] & b

    def borr(self, a, b, c):
        self.register[c] = self.register[a] | self.register[b]

    def bori(self, a, b, c):
        self.register[c] = self.register[a] | b

    def setr(self, a, b, c):
        self.register[c] = self.register[a]

    def seti(self, a, b, c):
        self.register[c] = a

    def gtir(self, a, b, c):
        self.register[c] = int(a > self.register[b])

    def gtri(self, a, b, c):
        self.register[c] = int(self.register[a] > b)

    def gtrr(self, a, b, c):
        self.register[c] = int(self.register[a] > self.register[b])

    def eqir(self, a, b, c):
        self.register[c] = int(a == self.register[b])

    def eqri(self, a, b, c):
        self.register[c] = int(self.register[a] == b)

    def eqrr(self, a, b, c):
        self.register[c] = int(self.register[a] == self.register[b])


def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            data.append(tuple(v if i==0 else int(v) for i, v in enumerate(ln.replace('\n', '').split())))

    # Part 1
    if False:
        comp = Comp(data.copy())
        comp.run()
        print(f"A1: {comp.register[0]}")

    # Part 2
    divisors = lambda n: set(chain.from_iterable((i,n//i) for i in range(1, math.isqrt(n)+1) if n%i == 0))

    comp = Comp(data.copy())
    comp.register[0] = 1
    comp.run()
    print(f"A2: {comp.register[0]}")

if __name__ == '__main__':
    main()
