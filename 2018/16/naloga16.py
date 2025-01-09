# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
from dataclasses import dataclass, field
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

@dataclass
class Comp:
    register: list = field(default_factory=lambda: [0 for k in range(4)])

    def __post_init__(self):
        pass

    def run(self, code):
        for step in code:
            getattr(self, step[0])(*step[1:])

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
    sample = []
    program = []
    program_ = False; ln_ = 0
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '':
                if (ln_ := ln_ + 1) >= 2:
                    program_ = True
                continue
            if program_:
                if ln != '':
                    program.append(tuple(int(i) for i in ln.split()))
            else:
                if ln.startswith('Before'):
                    da = {'before': tuple(int(i) for i in ln.replace('Before: [', '').replace(']','').split(','))}
                elif ln.startswith('After:'):
                    da.update({'after': tuple(int(i) for i in ln.replace('After:  [', '').replace(']','').split(','))})
                    sample.append(da)
                    ln_ = 0
                else:
                    da.update({'code': tuple(int(i) for i in ln.split())})

    # Part 1
    test = []
    for smpl in sample:
        tst = set()
        for opcode in {'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'}:
            getattr(x := Comp(list(smpl['before'])), opcode)(*smpl['code'][1:])
            if tuple(x.register) == smpl['after']:
                tst.add(opcode)
        test.append((smpl['code'][0], tst))
    print(f"A1: {sum(1 for _, i in test if len(i) >= 3)}")

    # Part 2
    opcode_ = {i: set.intersection(*tuple(s for i_,s in test if i_ == i)) for i in {i for i,_ in test}}
    opcode = {}
    while set(opcode) != set(opcode_):
        opcode |= {i: next(iter(c)) for i, c in opcode_.items() if len(c) == 1}
        opcode_ = {i: c - set(opcode.values()) for i, c in opcode_.items()}
    comp = Comp()
    comp.run([(opcode[p[0]],) + p[1:] for p in program])
    print(f"A2: {comp.register[0]}")

if __name__ == '__main__':
    main()
