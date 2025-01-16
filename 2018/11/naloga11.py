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
    serial = 9435
    #serial = 18

    nn = 300

    rack = np.array([[x+1+10 for x in range(nn)] for y in range(nn)])
    power = (((np.array([y+1 for y in range(nn)]).reshape((-1,1)) * rack + serial) * rack) // 100) % 10 - 5
    
    def max_power(n = 3):
        pw = {(x+1,y+1): int(power[y:y+n, x:x+n].sum()) for y in range(nn-n) for x in range(nn-n)}
        return sorted(pw.items(), key=lambda item: item[1], reverse=True)[0]
    
    # Part 1
    if True:
        p1 = max_power()
        print(f"A1: {','.join(str(i) for i in p1[0])}")

    # Part 2
    p2 = {}
    for k in range(1,nn):
        xy, v = max_power(k)
        p2.update({xy+(k,): v})
    p2 = sorted(p2.items(), key=lambda item: item[1], reverse=True)[0]
    print(f"A2: {','.join(str(i) for i in p2[0])}")

if __name__ == '__main__':
    main()
