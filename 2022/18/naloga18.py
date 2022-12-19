# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product
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
            da = ln.split(',')
            data += [tuple(int(i) for i in da)]

    def surface(droplet, mat = 0):
        surf = 0
        for x,y,z in zip(*np.where(droplet == 1)):
            surf += (droplet[x-1:x+2, y, z] == mat).sum()
            surf += (droplet[x, y-1:y+2, z] == mat).sum()
            surf += (droplet[x, y, z-1:z+2] == mat).sum()
        return surf

    def flood(droplet):
        plus = lambda x, y: (x[0]+y[0], x[1]+y[1], x[2]+y[2])
        
        droplet = copy.deepcopy(droplet)
        voda = 0
        for v in product(*tuple((0, droplet.shape[r]-1) for r in range(3))):
            droplet[v] = 2;
        while (droplet == 2).sum() != voda:
            voda = (droplet == 2).sum()
            for x,y,z in zip(*np.where(droplet == 2)):
                for d in (lambda I = (0,0,0): {I[:i]+(v,)+I[i+1:] for i in range(3) for v in {1,-1}})():
                    _xyz = plus((x,y,z), d)
                    try:
                        if droplet[_xyz] == 0: droplet[_xyz] = 2
                    except: IndexError
        return droplet

    # Part 1
    if True:
        dat=set(copy.deepcopy(data))
        bias = tuple(min(j[i] for j in dat) for i in range(3))
        dat = [tuple(i[j] - bias[j] + 1 for j in range(3)) for i in dat]
        kepa = np.zeros(tuple(max(j[i] for j in dat)+2 for i in range(3))).astype(int)
        for i in dat:
            kepa[i] = 1
        p1 = surface(kepa)
        print(f"A1: {p1}")

    # Part 2
    poplavljen = flood(kepa)
    p2 = surface(poplavljen, 2)
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
