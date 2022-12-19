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
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '').replace('Blueprint ','')
            _dat = ln.split(':')
            da = _dat[1].replace(': ','').split('.')
            dat = {'o': {'o': int(da[0].replace('Each ore robot costs', '').replace('ore',''))}}
            dat.update({'c': {'o': int(da[1].replace('Each clay robot costs', '').replace('ore',''))}})
            d = da[2].replace('Each obsidian robot costs', '').replace('ore and' , ' ').replace('clay','').split()
            dat.update({'b': {'o': int(d[0]), 'c': int(d[1])}})
            d = da[3].replace('Each geode robot costs', '').replace('ore and' , ' ').replace('obsidian','').split()
            dat.update({'g': {'o': int(d[0]), 'b': int(d[1])}})
            data.update({int(_dat[0]): dat})

    def delaj(rob, inv, plan, t = 0):
        inv = {k: r + inv.get(k,0) for k, r in rob.items()}
        opcije = []
        for kk in {'c', 'b', 'g'}:
            if inv[pnan['kk']] > plan['g']

    # Part 1
    tt = 24
    if True:
        for k, plan in data.items():
            rob = {'o': 1} | {k: 0 for k in {'c', 'b', 'g'}}
            inv = {k: 0 for k in {'o', 'c', 'b', 'g'}}
            delaj (rob, inv, plan)
            
            # clay = (co) * ore
            # obsi = (bo + bo*co) * ore
            # good = (go + gb*bo +gb*bo*co) * ore

        print(f"A1: {0}")

    # Part 2
    dat=copy.deepcopy(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
