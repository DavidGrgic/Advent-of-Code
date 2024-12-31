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
            ins, cond = ln.replace('\n', '').split(' if ')
            data.append(tuple(int(i) if i.lstrip('-').isdigit() else i for i in ins.split()) + (tuple(int(i) if i.lstrip('-').isdigit() else i for i in cond.split()),))


    # Part 1
    p2_max = None
    register = {}
    for reg, ins, val, cond in data:
        match cond:
            case r, '>', v:
                if not register.get(r, 0) > v:
                    continue
            case r, '<', v:
                if not register.get(r, 0) < v:
                    continue
            case r, '>=', v:
                if not register.get(r, 0) >= v:
                    continue
            case r, '<=', v:
                if not register.get(r, 0) <= v:
                    continue
            case r, '==', v:
                if not register.get(r, 0) == v:
                    continue
            case r, '!=', v:
                if not register.get(r, 0) != v:
                    continue
            case _:
                raise Exception()
        match ins:
            case 'inc':
                register[reg] = register.get(reg, 0) + val
            case 'dec':
                register[reg] = register.get(reg, 0) - val
            case _:
                raise Exception()
        tmp = max(register.values())
        if p2_max is None or tmp > p2_max:
            p2_max = tmp
    print(f"A1: {max(register.values())}")

    # Part 2
    print(f"A2: {p2_max}")

if __name__ == '__main__':
    main()
