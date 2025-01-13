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

    def run(self, debug: tuple[int] = None):
        if debug:
            if not hasattr(debug, '__iter__'):
                debug = (0, debug)
        pointer = 0
        nn = 0
        while pointer in self.code and (not debug or nn <= debug[-1]):
            self.register[self.bound] = pointer
            step = self.code[pointer]
            if debug and debug[0] <= nn:
                print(f"{nn}: {pointer}", self.register, step, end=' ')
            getattr(self, step[0])(*step[1:])
            if debug and debug[0] <= nn:
                print(self.register)
            pointer = self.register[self.bound]
            pointer += 1
            nn += 1

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
        comp = Comp(data.copy())
        comp.run()
        print(f"A1: {comp.register[0]}")

    # Part 2
    """
    Za primer pod part 1 (torej ko se začne z registorm 0 z redenostjo 0), če poženeš program z ispisom vrednsoti registrov:
        comp = Comp(data.copy()); comp.run((0,1000))
    Je po nekaj korakih (21 korak) očitno, da obstaja loop ko pointer teče od 3 do 11. Poleg tega ima zadnji register neko vrednost, v konkretnem primeru 931, predzadnji register se v vsakem loopu poveča za 1
    Če si izpišemo malo bolj poznejši del, ko se predzadnji register približa vrednosti zadnjega registra:
        comp = Comp(data.copy()); comp.run((7440,8000))
    V koraku 7449 doseže predzadnji register vrednost zadnjega registra in v 7456 koraku se v register 0 zapiše vrednost 1, predzadnji register se postavi na 1 in loop se začne ponovno
    Naslednjič doseže predzadnji register vrednost 931 v koraku 14901, vendar se po tem vresnost registra 0 ne poveča:
        comp = Comp(data.copy()); comp.run((14900,15000))
    Naslednjič, ko se register 0 spremeni je okoli koraka 45784, ko se poveča za 7, na vrednost 8:
        comp = Comp(data.copy()); comp.run((45780, 45800))
    Ter ponovno v okolici koraka 134536, ko se poveča za 19, na 27:
        comp = Comp(data.copy()); comp.run((134520, 134600))
    Ter ponovno v okolici koraka 357856, ko se poveča za 49, na 76:
        comp = Comp(data.copy()); comp.run((357850, 357900))
    itd.
    Register 0 se torej povečuje: 1, 7, 19, 49,... kar so ravno celoštevilski deljitelji števila 931, vsota vseh deljitevlejv pa je na koncu 1140, kar je rezultat prvega dela naloge.
    Če zavrtimo nekaj korakov drugega dela naloge:
        comp = Comp(data.copy()); comp.register[0] = 1; comp.run((0,1000))
    Vidimo, da se po uvodni inicalizaciji postavi zadnji register na 10551331, od koraka 21 naprej pa se ponovno začne enak loop kot za prvi del naloge.
    Poiščemo torej vse celoštevilska seljitelje števila 10551331 in njihov seštevek je rezultat drugega dela naloge.
    """
    divisors = lambda n: set(chain.from_iterable((i,n//i) for i in range(1, math.isqrt(n)+1) if n%i == 0))
    p2 = divisors(10551331)
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()
