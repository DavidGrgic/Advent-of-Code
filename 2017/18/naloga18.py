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


class Comp:
    
    def __init__(self, code, register = None):
        self.code = code
        self.register = {} if register is None else register
        self.position = 0  # If position is None, program is terinated
        self._queue = []
        self._output = []
        self.n_send = 0
    
    def run(self, _queue = None):
        if _queue is not None:
            self.queue(_queue)
        while self.position in self.code:
            match self.code[self.position]:
                case 'snd', x:
                    self._output.append(self.register.get(x, x))
                    self.n_send += 1
                case 'set', x, y:
                    self.register[x] = self.register.get(y, y)
                case 'add', x, y:
                    if x not in self.register: self.register[x] = 0
                    self.register[x] += self.register.get(y, y)
                case 'mul', x, y:
                    if x not in self.register: self.register[x] = 0
                    self.register[x] *= self.register.get(y, y)
                case 'mod', x, y:
                    if x not in self.register: self.register[x] = 0
                    self.register[x] %= self.register.get(y, y)
                case 'rcv', x:
                    if len(self._queue) > 0:
                        self.register[x] = self._queue.pop(0)
                    else:
                        break
                case 'jgz', x, y:
                    if self.register.get(x, x) > 0:
                        self.position += self.register.get(y, y)-1
                case _:
                    raise Exception()
            self.position += 1
        else:
            self.position = None
        
    def queue(self, _queue):
        self._queue.extend(_queue)
        
    def output(self, consume = True):
        ret = self._output.copy()
        if consume:
            self._output = []
        return ret


def main():
    # Read
    code = {}
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            ixy = ln.replace('\n', '').split()
            code.update({i: (ixy[0],) + tuple(int(k) if k.lstrip('-').isdigit() else k for k in ixy[1:])})

    def recover(reg = None, pos = 0):
        if reg is None:
            reg = {}
        sound = None
        while pos in code:
            match code[pos]:
                case 'snd', x:
                    sound = reg.get(x, x)
                case 'set', x, y:
                    reg[x] = reg.get(y, y)
                case 'add', x, y:
                    if x not in reg: reg[x] = 0
                    reg[x] += reg.get(y, y)
                case 'mul', x, y:
                    if x not in reg: reg[x] = 0
                    reg[x] *= reg.get(y, y)
                case 'mod', x, y:
                    if x not in reg: reg[x] = 0
                    reg[x] %= reg.get(y, y)
                case 'rcv', x:
                    if reg.get(x, x):
                        break
                case 'jgz', x, y:
                    if reg.get(x, x) > 0:
                        pos += reg.get(y, y)-1
                case _:
                    raise Exception()
            pos += 1
        return sound

    # Part 1
    if True:
        print(f"A1: {recover()}")

    # Part 2
    comp = {k: Comp(code, {'p': k}) for k in range(2)}
    while all(c.position is not None for c in comp.values()):
        for k in range(len(comp)):
            comp[k].run()
            comp[(k+1)%2].queue(comp[k].output())
        if all(len(c._queue) == 0 for c in comp.values()):
            break
    print(f"A2: {comp[1].n_send}")

if __name__ == '__main__':
    main()
