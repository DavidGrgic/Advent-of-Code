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
    data = 1024
    data = 277678

    plus = lambda t, s: (t[0] + s[0], t[1] + s[1])
    adj = lambda a, b: max(abs(a[0]-b[0]), abs(a[1]-b[1])) == 1

    # Part 1
    if True:
        smer = [(1,0), (0,1), (-1,0), (0,-1)]
        smer_id = 0
        s = steps = 1
        c = 2
        tocka = (0,0)
        sekvenca = [tocka]
        for i in range(2, data+1):
            tocka = plus(tocka, smer[smer_id])
            sekvenca.append(tocka)
            s -= 1
            if s == 0:
                smer_id = (smer_id + 1) % 4
                c -= 1
                if c == 0:
                    c = 2
                    steps += 1
                s = steps
        print(f"A1: {abs(tocka[0]) + abs(tocka[1])}")

    # Part 2
    i = 0
    polje = {sekvenca[i]: 1}
    while True:
        i += 1
        value = sum([v for p, v in polje.items() if adj(sekvenca[i], p)])
        if value > data:
            break
        polje.update({sekvenca[i]: value})
    print(f"A2: {value}")

if __name__ == '__main__':
    main()
