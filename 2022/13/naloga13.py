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
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():
    # Read
    data = {}
    dat = ()
    k = 1
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                data.update({k: dat})
                dat = ()
                k += 1
                continue
            dat += (eval(ln),)
    if len(dat) == 2:
        data.update({k: dat})

    def compare(le, ri):
        l = copy.deepcopy(le); r = copy.deepcopy(ri)
        if isinstance(l, int):
            l = [l]
        if isinstance(r, int):
            r = [r]
        for i in range(len(l)):
            if len(r) < i+1:
                return False
            if sum((isinstance(l[i], list), isinstance(r[i], list))) >= 1:
                ret = compare(l[i], r[i])
                if isinstance(ret, bool):
                    return ret
                else:
                    continue
            if l[i] == r[i]:
                continue
            elif l[i] < r[i]:
                return True
            else:
                return False
        if len(l) < len(r):
            return True
        return None

    # Part 1
    if True:
        p1 = set()
        for k, v in data.items():
            pp = compare(*v)
            if pp is None:
                p1 |= {k}
            elif pp:
                p1 |= {k}
        print(f"A1: {sum(p1)}")

    # Part 2
    dod = [  [[2]]  ,  [[6]]  ]
    dat = [j for k, v in data.items() for j in v] + dod
    k = 0
    while k < len(dat)-1:
        _l = copy.deepcopy(dat[k])
        _r = copy.deepcopy(dat[k+1])
        if compare(_l,_r):
            k += 1
        else:
            dat[k] = _r
            dat[k+1] = _l
            k = max(k-1,0)
    print(f"A2: {math.prod(list(dat).index(i)+1 for i in dod)}")

if __name__ == '__main__':
    main()
