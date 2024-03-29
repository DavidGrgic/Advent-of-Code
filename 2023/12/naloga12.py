﻿# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys, time
import pandas as pd, numpy as np
from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product
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
            da = ln.split(' ')
            data += [(da[0], tuple(int(i) for i in da[1].split(',')))]

    kesh = {}
    def generiraj(niz, num):
        if (niz, num) in kesh:
            return kesh[(niz, num)]
        if len(num) == 0:
            stej = int(niz.find('#') < 0)
        else:
            pos = niz.find('?')
            if pos < 0:
                stej = int(tuple(len(i) for i in niz.replace('.', ' ').split()) == num)
            else:
                stej = 0
                for zna in {'.', '#'}:
                    kandidat = ''.join(zna if i == pos else v for i, v in enumerate(niz)).strip()
                    test = kandidat.replace('.', ' ').split()
                    if len(test) > 0 and set(test[0]) == {'#'}:
                        if len(test[0]) == num[0]:
                            stej += generiraj('.'.join(test[1:]), num[1:])
                    else:
                        stej += generiraj('.'.join(test), num)
        kesh[(niz, num)] = stej
        return stej

    # Part 1
    if True:
        p1 = []
        for spr, num in data:
            ok = 0
            poz = [i for i, v in enumerate(spr) if v == '?']
            comb = [str(bin(i))[2:].replace('0','.').replace('1','#') for i in range(2**len(poz))]
            ln = len(comb[-1])
            comb = [(ln - len(i))*'.'+i for i in comb]
            for co in comb:
                test = ''.join(co[poz.index(i)] if i in poz else v for i, v in enumerate(spr))
                test = test.replace('.',' ').split()
                if len(test) != len(num):
                    continue
                if tuple(len(i) for i in test) == num:
                    ok += 1
            p1.append(ok)
        print(f"A1: {sum(p1)}")

    # Part 2
    nn = 5
    p2 = []
    for sprr, numm in data:
        ok = 0
        spr = '?'.join(sprr for _ in range(nn))
        num = nn * numm
        p2.append(generiraj(spr, num))
        #print(f"{len(p2)}/{len(data)}: {p2[-1]}")
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()
