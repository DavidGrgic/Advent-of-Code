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
            data += [int(ln.replace('\n', ''))]

    def after(wrap, ite, n = 0):
        p = show(wrap).index(0)
        return wrap[(p+ite) % len(wrap)][1]

    show = lambda wrap: [i[1] for i in wrap]

    def mix(data = data, num = 1):
        wrap = [(i, v) for i, v in enumerate(data)]
        _wrap = copy.deepcopy(wrap)
        l = len(wrap)
        for _ in range(num):
            for i, _m in _wrap:
                if _m % l == 0:
                    continue
                elif _m < 0: # Premakni v levo
                    levo = True
                    m = -_m
                    wrap = wrap[::-1]
                else:
                    levo = False
                    m = _m
                p = wrap.index((i,_m))
                wrap = wrap[:p] + wrap[p+1:]
                m = (p + m) % (l-1)
                wrap = wrap[:m] + [(i,_m)] + wrap[m:]
                if levo:
                    wrap = wrap[::-1]
        return wrap

    # Part 1
    if True:
        wrp = mix(data)
        print(f"A1: {sum(after(wrp, i * 1000) for i in range(1,4))}")

    # Part 2
    key = 811589153
    dat = [i * key for i in data]
    wrp = mix(dat, 10)
    print(f"A2: {sum(after(wrp, i * 1000) for i in range(1,4))}")

if __name__ == '__main__':
    main()
