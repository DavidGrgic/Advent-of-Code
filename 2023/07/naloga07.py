# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from collections import Counter
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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split()
            data += [(da[0], int(da[1]))]

    def primerjaj(x, y, pwr, xx = None, yy = None):
        def enaka():
            for i, j in zip(xx,yy):
                if i == j:
                    continue
                elif pwr.index(i) < pwr.index(j):
                    return True
                else:
                    return False
            raise AssertionError
        
        if xx is None:
            xx = x
        if yy is None:
            yy = y
        x_ = sorted(Counter(x).values(), reverse = True)
        y_ = sorted(Counter(y).values(), reverse = True)
        if x_[0] > y_[0]:
            return True
        elif x_[0] == y_[0]:
            if len(x_) == 1 and len(y_) == 1:
                return enaka()
            elif len(x_) == 1:
                return True
            elif len(y_) == 1:
                return False
            elif x_[1] > y_[1]:
                return True
            elif x_[1] == y_[1]:
                return enaka()
            else:
                return False
        else:
            return False
        raise AssertionError

    def uredi(dat, pwr):
        k = 0
        while k < len(dat) - 1:
            red = primerjaj(*((dat[k][0], dat[k+1][0], pwr) + ((dat[k][2], dat[k+1][2]) if len(dat[k]) == 3 else ())))
            if red:
                k += 1
            else:
                dat = dat[:k] + [dat[k+1], dat[k]] + dat[k+2:]
                k -= 1
            k = max(0 , k)
        return dat

    def strong(v):
        ret = v
        for i in power2[:-1]:
            if i not in ret:
                continue
            kan = v.replace(i, 'J')
            if primerjaj(kan, ret, power2):
                ret = kan
        return ret

    # Part 1
    if True:
        power1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        dat =  copy.deepcopy(data)
        p1 = [(i+1, v[1]) for i, v in enumerate(uredi(dat, power1)[::-1])]
        print(f"A1: {sum(math.prod(i) for i in p1)}")

    # Part 2
    power2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    dat = []
    for k in data:
        dat.append((strong(k[0]), k[1], k[0]))
    p2 = [(i+1, v[1]) for i, v in enumerate(uredi(dat, power2)[::-1])]
    print(f"A2: {sum(math.prod(i) for i in p2)}")

if __name__ == '__main__':
    main()
