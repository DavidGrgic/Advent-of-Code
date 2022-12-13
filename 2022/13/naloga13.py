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


    def compare(le, ri):
        l = copy.deepcopy(le); r = copy.deepcopy(ri)
        ret = None
        if isinstance(l, int):
            l = [l]
        if isinstance(r, int):
            r = [r]
        for i in range(len(l)):
            if len(r) < i+1:
                ret = False
                break
            if sum((isinstance(l[i], list), isinstance(r[i], list))) >= 1:
                re = compare(l[i], r[i])
                if isinstance(re, bool):
                    ret = re
                    break
                else:
                    continue
            if l[i] == r[i]:
                continue
            elif l[i] < r[i]:
                ret = True
                break
            else:
                ret = False
                break
        if ret is None and len(r) > len(l):
            ret = True
        return ret

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
        #5675

    # Part 2
    dat=copy.deepcopy(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
