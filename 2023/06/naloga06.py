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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [int(i) for i in ln.split(': ')[-1].split()]
            data += [da]

    def naloga_(time, dist):
        pp = []
        for t, d in zip(time, dist):
            k = 1
            over = False
            p = 0
            while k < d:
                x = (t-k) * k
                if x > d:
                    p += 1
                    over = True
                elif over:
                    break
                k += 1
            pp.append(p)
        return pp
    
    def naloga(time, dist):
        kvad = lambda t, d: tuple((t + i*math.sqrt(t**2 - 4* d))/2 for i in (1,-1))
        eps = 1e-12
        pp = []
        for t, d in zip(time, dist):
            x = kvad(t,d)
            k = math.floor(x[0] - eps) - math.ceil(x[1] + eps) + 1
            pp.append(max(k,0))
        return pp

    # Part 1
    if True:
        p1 = naloga(data[0], data[1])
        #p1 = naloga_(data[0], data[1])
        print(f"A1: {math.prod(p1)}")

    # Part 2
    p2 = naloga(*tuple([int(''.join(str(i) for i in data[j]))] for j in range(2)))
    #p2 = naloga_(*tuple([int(''.join(str(i) for i in data[j]))] for j in range(2)))
    print(f"A2: {math.prod(p2)}")

if __name__ == '__main__':
    main()
