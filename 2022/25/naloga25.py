# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
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
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                pass
            data += [ln]

    con = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    noc = {v: k for k, v in con.items()}

    def decode(snafu):
        res = 0
        for i, v in enumerate(snafu[::-1]):
            res += (5**i) * con[v]
        return res

    def code(num):
        nu = num
        res = []; i = 0
        while True:
            nu += 2*(5**i)
            res.append((nu // (5**i)) % 5)
            if 5**i > num:
                break
            i += 1
        res = ''.join([noc[i-2] for i in res[::-1]])
        while res[0] == '0':
            res = res[1:]
        return res

    # Part 1
    fuel = 0
    for i in data:
        fuel += decode(i)
    p1 = code(fuel)
    print(f"A1: {p1}")


if __name__ == '__main__':
    main()
