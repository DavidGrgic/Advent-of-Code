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
    data = {}
    instruction = {}
    with open('d.txt', 'r') as file:
        for l, ln in enumerate(file):
            match ln.replace('\n', '').split():
                case 'value', v, 'goes', 'to', 'bot', b:
                    b = int(b)
                    data.update({b: data.get(b, set()) | {int(v)}})
                case 'bot', b, 'gives', 'low', 'to', l, l_, 'and', 'high', 'to', h, h_:
                    instruction.update({int(b): ((l, int(l_)), (h, int(h_)))})
                case _:
                    raise Exception('Unknown imput.')

    goal = {17,61} if len(data) > 5 else {2,5}

    # Part 1
    dat = copy.deepcopy(data)
    out = {}
    while (todo := {k: sorted(v) for k, v in dat.items() if len(v) == 2}):
        if (goal_ := [k for k, v in dat.items() if v == goal]):
            p1 = goal_
        for k, v in todo.items():
            for i_, v_ in zip(instruction[k], v):
                match i_:
                    case 'bot', x:
                        dat.update({x: dat.get(x, set()) | {v_}})
                    case 'output', x:
                        out.update({x: out.get(x, []) + [v_]})
                    case _:
                        raise Exception(f"Unknown instruction '{i_}'")
            dat[k] = set()
    print(f"A1: {next(iter(p1))}")

    # Part 2
    print(f"A2: {math.prod(next(iter(v)) for k, v in out.items() if k in {0,1,2})}")

if __name__ == '__main__':
    main()
