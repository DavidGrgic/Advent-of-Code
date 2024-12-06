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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [i == '#' for i in ln]
            data += [da]
            p = ln.find('^')
            if p >= 0:
                start = (c, p)
    data = np.array(data)
    dim_x, dim_y = data.shape
    ovire = {(int(x),int(y)) for x,y in zip(*np.where(data))}
    prosti = {(i, j) for i in range(dim_x) for j in range(dim_y)} - ovire - {start}
    
    plus = lambda xy, di: (xy[0]+di[0], xy[1]+di[1])
    turn = {0:(-1,0), 1:(0,1), 2:(1,0), 3:(0,-1)}
    
    def pot(xyd, ovi):

        def korak(xyd):
            xy = plus(xyd[:2], turn[xyd[-1]])
            return korak(xyd[:2] + ((xyd[-1] + 1) % 4,)) if xy in ovi else xy + (xyd[-1],)

        pot_ = {xyd}
        while True:
            xyd = korak(xyd)
            if xyd in pot_:  # Loop
                return
            if xyd[0] >= dim_x or xyd[1] >= dim_y or xyd[0] < 0 or xyd[1] < 0:
                return pot_
            pot_ |= {xyd}

    # Part 1
    if True:
        p1 = pot(start + (0,), ovire)
        print(f"A1: {len({i[:2] for i in p1})}")

    # Part 2
    p2 = set()
    for dod in prosti:
        if pot(start + (0,), ovire | {dod}) is None:
            p2 |= {dod}
    print(f"A2: {len(p2)}")

if __name__ == '__main__':
    main()
