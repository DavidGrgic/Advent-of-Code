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

    def run(self, debug: tuple[int] = None, debug_pointer: set[int] = None):
        if debug:
            if not hasattr(debug, '__iter__'):
                debug = (0, debug)
        pointer = 0
        nn = 0
        while pointer in self.code and (not debug or nn <= debug[-1]):
            self.register[self.bound] = pointer
            step = self.code[pointer]
            show = debug and debug[0] <= nn and (debug_pointer is None or pointer in debug_pointer)
            if show:
                print(f"{nn}: {pointer}", self.register, step, end=' ')
            getattr(self, step[0])(*step[1:])
            if show:
                print(self.register)
            pointer = self.register[self.bound]
            pointer += 1
            nn += 1

    def run28(self):
        register3 = []
        pointer = 0
        nn = 0
        while pointer in self.code:
            self.register[self.bound] = pointer
            if pointer == 28:
                register3.append((nn, self.register[3]))
                if register3[-1][-1] in {i[-1] for i in register3[:-1]}:
                    break
            step = self.code[pointer]
            getattr(self, step[0])(*step[1:])
            pointer = self.register[self.bound]
            pointer += 1
            nn += 1
        return register3

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
    if True:
        """
        Register se 0 se uporablja zgolj v 28 vrstici programa, ko se primerja z registrom 3, torej koda: ('eqrr', 3, 0, 1)
        Prvič se to zgodi v koraku 1846:
            comp = Comp(data.copy()); comp.run(10**4, {28})
        Takrat ima register 3 vrednost 212115 in če bo tudi register 0 imel to vrednost, se bo nekaj zgodilo... najbrž se bo program ustavil,
        kar perverimo spodaj, torej če se bo program ustavil ko poženemo comp.run(), potem je to rezultat prvega dela naloge:
        """
        comp = Comp(data.copy())
        p1 = 212115
        comp.register[0] = p1
        comp.run()
        print(f"A1: {p1}")

    # Part 2
    comp = Comp(data.copy())
    p2 = comp.run28()
    print(f"A2: {p2[-2][-1]}")

if __name__ == '__main__':
    main()
