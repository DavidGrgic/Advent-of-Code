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
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split('~')
            data.update({c+1: [tuple(int(j) for j in i.split(',')) for i in da]})

    def padec(dat):
        z = 1
        while z < dat.shape[2]:
            plast = dat[:,:,z]
            bri = set(i for j in plast for i in j) - {0}
            premik = False
            for br in bri:
                xy = np.where(plast == br)
                if (dat[xy+(z-1,)] == 0).all():
                    xyz = np.where(dat == br)
                    dat[xyz] = 0
                    dat[tuple(d-1 if i ==2 else d for i,d in enumerate(xyz))] = br
                    premik = True
            if premik:
                if z > 1:
                    z -= 1
            else:
                z += 1
        return dat
        
    dat = np.zeros(tuple(max(i[d] for v in data.values() for i in v)+1 for d in range(3)), dtype = int)  # (z, y, x)
    for idx, brick in data.items():
        for x in range(brick[0][0], brick[1][0]+1):
            for y in range(brick[0][1], brick[1][1]+1):
                for z in range(brick[0][2], brick[1][2]+1):
                    dat[x,y,z] = idx
    dat = padec(dat)
    # Part 1
    if True:
        p1 = []
        for idx, brick in data.items():
            print(idx)
            dat_ = dat.copy()
            dat_[np.where(dat_ == idx)] = 0
            dat__ = padec(dat_.copy())
            if (dat__ == dat_).all():
                p1.append(idx)
        print(f"A1: {len(p1)}")

    # Part 2
    p2 = {}
    for idx in set(data.keys()) - set(p1):
        print(idx)
        dat_ = dat.copy()
        dat_[np.where(dat_ == idx)] = 0
        dat__ = padec(dat_.copy())
        fall = []
        for br in data:
            if not all((a == b).all() for a, b in zip(np.where(dat_ == br), np.where(dat__ == br))):
                fall.append(br)
        p2.update({idx: fall})
    print(f"A2: {sum(len(i) for i in p2.values())}")

if __name__ == '__main__':
    main()
