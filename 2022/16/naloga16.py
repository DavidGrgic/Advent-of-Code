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
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    data = {}
    with open('t.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(';')
            kn = da[0].split(' has flow rate=')
            k = kn[0].replace('Valve ','')
            m = da[1].replace(' tunnels lead to valves ', '').replace(' tunnel leads to valve ', '').split(', ')
            data.update({k: (int(kn[1]), set(m))})

    tt = 15

    def poti(vv, t = -1, obiskani = set(), nazaj = set()):
        t += 1
        obiskani |= {vv}
        if t >= tt:
            return {((vv, False, t),)}
        pot = set()
        for odprt in {True, False}:
            if odprt:
                t += 1
                if t >= tt:
                    return {((vv, False, t),)}
            po = []
            for i in dat[vv][1] - (obiskani - nazaj):
                po = poti(i, t, obiskani, {vv})
            if len(po) == 0:
                pot |= {((vv, False, t),)}
            else:
                pot |= {((vv, odprt, t),) + i for i in po}
        return pot
        

    # Part 1
    if True:
        dat=copy.deepcopy(data)
        p1 = poti('AA')
        print(f"A1: {0}")

    # Part 2
    dat=copy.deepcopy(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
