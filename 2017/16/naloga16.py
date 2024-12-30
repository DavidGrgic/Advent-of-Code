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

def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            data.extend(ln.replace('\n', '').split(','))
    data = [(d[0], tuple(int(i) if d[0] == 'x' else i for i in d[1:].split('/')) if d[0] != 's' else int(d[1:])) for d in data]

    def dance(program):
        for dat in data:
            match dat:
                case 's', n:
                    program = program[-n:] + program[:-n]
                case 'x', (i, j):
                    program[i], program[j] = program[j], program[i]
                case 'p', (i, j):
                    program = [j if v == i else (i if v == j else v) for v in program]
                case _:
                    raise Exception()
        return program

    program = [chr(ord('a')+i)for i in range(16 if len(data) > 10 else 5)]

    # Part 1
    if True:
        p1 = dance(program.copy())
        print(f"A1: {''.join(p1)}")

    # Part 2
    nn = 1000000000
    sequence = []
    while (prog := ''.join(program)) not in sequence:
        sequence.append(prog)
        program = dance(program)
    p2 = sequence[nn % len(sequence)]
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
