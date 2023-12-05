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
    seeds = []
    maps = {}
    text = False
    with open('t.txt', 'r') as file:
        step = -1
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if len(seeds) == 0:
                seeds = [int(i) for i in ln.split(': ')[1].split()]
                continue
            if ln == ''  or text: # Nov blok podatkov
                if text:
                    step += 1
                text = not text
                continue
            da = [int(i) for i in ln.split()]
            maps.update({step: maps.get(step, []) + [tuple(da)]})

    # Part 1
    if True:
        def preslikaj(value, step):
            mm = maps[step]
            for m in mm:
                if m[1] <= value < (m[1] + m[2]):
                    return value - m[1] + m[0]
            return value
        
        def search(value, step = 0):
            if step in maps:
                return search(preslikaj(value, step), step + 1)
            else:
                return value
       
        p1 = []
        for ss in seeds:
            res = search(ss)
            p1.append(res)
        print(f"A1: {min(p1)}")

    # Part 2
    semena = [range(seeds[i], seeds[i] + seeds[i+1])for i in range(0, len(seeds), 2)]

    def slikaj(value, step):
        mm = maps[step]
        ret = []
        for m in mm:
            if min(value) < m[1]:
                if max(value) >= m[1]:
                    if max(value) <= m[1]+m[2]:
                        return [range(min(value), m[1]), range(m[1], min(m[1]+m[2], max(value)))]
                    else:
                        pass
            if m[1] <= value < (m[1] + m[2]):
                return value - m[1] + m[0]
        return value

    def isci(value, step = 0):
        if step in maps:
            res = []
            for val in value:
                slikaj(val, step)
            return isci(res, step + 1)
        else:
            return value
    
    p2 = isci(semena)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
