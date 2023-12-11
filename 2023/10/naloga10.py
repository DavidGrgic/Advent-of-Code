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
_img_map = {0: ' ', 1: '.', 2: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
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
            data += [ln]

    plus = lambda x, y: (x[0] + y[0], x[1] + y[1])

    pipe = {(-1,0,'|'): (-1,0),
            (-1,0,'7'): (0,-1),
            (-1,0,'F'): (0,1),
            (1,0,'|'): (1,0),
            (1,0,'J'): (0,-1),
            (1,0,'L'): (0,1),
            (0,-1,'-'): (0,-1),
            (0,-1,'L'): (-1,0),
            (0,-1,'F'): (1,0),
            (0,1,'-'): (0,1),
            (0,1,'7'): (1,0),
            (0,1,'J'): (-1,0)}

    start = None
    for i, row in enumerate(data):
        j = row.find('S')
        if j >= 0:
            start = (i, j)
            break
        
    # Part 1
    if True:
        poti = []
        for k, smer in enumerate([(1,0), (0,1), (-1,0), (0,-1)]):
            pot = []
            tocka = start
            ok = True
            while True:
                tocka = plus(tocka, smer)
                if not (0 <= tocka[0] < len(data) and 0 <= tocka[1] < len(data[0])):
                    ok = False
                    break
                val = data[tocka[0]][tocka[1]]
                pot.append(tocka)
                if val == 'S':
                    break
                smer = pipe.get(smer + (val,))
                if smer is None:
                    ok = False
                    break
            if ok:
                poti.append(pot)
        p1 = [len(i)//2 for i in poti]
        print(f"A1: {max(p1)}")

    # Part 2
    dat = sorted(poti, key = lambda x: len(x))[-1]
    polje = np.zeros((len(data), len(data[0])), dtype = int)
    for ij in dat:
        polje[ij] = 1

    levo = {(1,0): [(0,1),(-1,1)],
            (0,-1): [(1,0),(1,1)],
            (-1,0): [(0,-1),(1,-1)],
            (0,1): [(-1,0),(-1,-1)]}

    zemljevid = []
    for pot in [dat, dat[::-1]]:
        zem = copy.deepcopy(polje)
        for k in range(1, len(pot)):
            smer = plus(pot[k], (-pot[k-1][0], -pot[k-1][1]))
            for ll in levo[smer]:
                tocka = plus(pot[k], ll)
                if not (0 <= tocka[0] < len(data) and 0 <= tocka[1] < len(data[0])):
                    continue
                if zem[tocka] == 0:
                    zem[tocka] = 2
        dvojk = (zem == 2).sum()
        znotraj = True
        while True:
            ij = np.where(zem == 2)
            for i, j in zip(*ij):
                for s in levo:
                    tocka = plus((i,j), s)
                    if not (0 <= tocka[0] < len(data) and 0 <= tocka[1] < len(data[0])):
                        znotraj = False
                        break
                    if zem[tocka] == 0:
                        zem[tocka] = 2
                if not znotraj:
                    break
            if (zem == 2).sum() == dvojk or not znotraj:
                break
            else:
                dvojk = (zem == 2).sum()
        if znotraj:
            zemljevid.append(zem)
    p2 = [(i==2).sum() for i in zemljevid]
    print(f"A2: {' '.join(str(i) for i in sorted(p2))}")

if __name__ == '__main__':
    main()
