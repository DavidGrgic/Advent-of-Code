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
    data = {}
    with open('t.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(': ')
            if len(da[1]) == 11:
                d = (da[1][:4], da[1][5], da[1][7:])
            else:
                d = int(da[1])
            data.update({da[0]: d})

    def racun(monk, dat):
        arg = dat[monk]
        if isinstance(arg, int):
            return arg
        elif isinstance(arg, tuple) and len(arg) == 3:
            a = racun(arg[0], dat)
            b = racun(arg[2], dat)
            return int(eval(f"{a}{arg[1]}{b}"))

    def subdat(monk, d = {}):
        arg = dat[monk]
        d = {monk: arg}
        if isinstance(arg, tuple) and len(arg) == 3:
            d.update(subdat(arg[0]) | subdat(arg[2]))
        return d
            
    def nazaj(cilj, monk, dat):
        if monk == 'humn':
            return cilj
        arg = dat[monk]
        if isinstance(arg, tuple) and len(arg) == 3:
            dat1 = subdat(arg[0])
            dat2 = subdat(arg[2])
            if 'humn' in dat1:
                dat_h = dat1
                humn = e1
                monk = e2
            elif 'humn' in dat2:
                dat_h = dat2
                humn = e2
                monk = e1
            else:
                raise AssertionError()
            cifra = racun(monk, dat)
            res = nazaj(cifra, humn, dat_h)
        else:
            res = arg
        print()
        

    # Part 1
    if True:
        dat=copy.deepcopy(data)
        p1 = racun('root', dat)
        print(f"A1: {p1}")

    # Part 2
    e1 = dat['root'][0]
    e2 = dat['root'][2]
    dat1 = subdat(e1)
    dat2 = subdat(e2)
    if 'humn' in dat1:
        dat_h = dat1
        humn = e1
        monk = e2
    elif 'humn' in dat2:
        dat_h = dat2
        humn = e2
        monk = e1
    else:
        raise AssertionError()
    cifra = racun(monk, dat)
    p2 = nazaj(cifra, humn, dat_h)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
