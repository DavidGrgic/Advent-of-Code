# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
#_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
#def _dict2img(x):
#    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
#    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
#    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
#    return img

def main():
    # Read
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split('>, ')
            data.update({c: [[int(i) for i in da[0][3:].split(',')], [int(i) for i in da[1][3:].split(',')], [int(i) for i in da[2][3:-1].split(',')]]})


    def clos(data):
        ac = {k: sum(abs(j) for j in v[2]) for k, v in data.items()}
        ac_min = min(ac.values())
        ac = {k for k, v in ac.items() if v == ac_min}
        vl = {k: sum(abs(j) for j in v[1]) for k, v in data.items() if k in ac}
        vl_min = [k for k, v in sorted(vl.items(), key = lambda x: x[1])]
        return vl_min[0]

    # Part 1
    p1 = clos(data)
    print(f"A1: {p1}")


    # Part 2
    plus = lambda x, y: (x[0]+y[0], x[1]+y[1], x[2]+y[2])
    dat = copy.deepcopy(data)
    for _ in range (100):
        vel = {k: plus(v[1], v[2]) for k, v in dat.items()}
        pos = {k: plus(v[0], vel[k]) for k, v in dat.items()}
        remain = {k for k, v in Counter(pos.values()).items() if v <= 1}
        dat = {k: [pos[k], vel[k], v[2]] for k, v in dat.items() if pos[k] in remain}
        #print(len(dat))
    print(f"A2: {len(dat)}")

if __name__ == '__main__':
    main()
