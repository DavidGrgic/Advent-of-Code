# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
from functools import cache   # @cache
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
    data = {}
    da = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if c == 0:
                state = ln[-2]
            elif c == 1:
                steps = int(ln.split(' ')[-2])
            else:
                if ln == '':
                    pass
                elif ln.startswith('In state'):
                    sta = ln[-2]
                elif ln.lstrip(' ').startswith('If the current value is'):
                    if len(da) > 0:
                        data |= da
                    val = int(ln[-2])
                    da = {(sta, val): 3 * [None]}
                elif ln.lstrip(' ').startswith('- Write the value'):
                    da[(sta, val)][0] = int(ln[-2])
                elif ln.lstrip(' ').startswith('- Move one slot to the '):
                    da[(sta, val)][1] = 1 if ln.find('right') >= 0 else -1
                elif ln.lstrip(' ').startswith('- Continue with state'):
                    da[(sta, val)][2] = ln[-2]
                else:
                    raise Exception
    data |= da

    # Part 1
    tape = {}
    position = 0
    for _ in range(steps):
        write, move, state = data[(state, tape.get(position, 0))]
        tape.update({position: write})
        position += move
    print(f"A1: {sum(tape.values())}")


if __name__ == '__main__':
    main()
