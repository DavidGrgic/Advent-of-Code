# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
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
    with open('t.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' ')
            data += [(da[0], tuple(int(i) for i in da[1].split(',')))]

    stej = lambda x: sum(i == '#' for i in x)

#    kash = {}
    def komb(niz):
#        niz = ''
#        if niz in kash:
#            return kash[niz]
        poz = [i for i, v in enumerate(niz) if v == '?']
        if len(poz) == 0:
            comb = {niz}
        else:
            try:
                comb = [str(bin(i))[2:].replace('0','.').replace('1','#') for i in range(2**len(poz))]
            except Exception as e:
                print(niz)
                raise e
            ln = len(comb[-1])
            comb = {(ln - len(i))*'.'+i for i in comb}
            comb = {''.join(co[poz.index(i)] if i in poz else v for i, v in enumerate(niz)) for co in comb}
        res = Counter([tuple(len(j) for j in i.replace('.', ' ').split()) for i in comb])
#        kash[niz] = res
        return res

    # Part 1
    if False:
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
        spr = spr.replace('.', ' ').split()
        kombinacije = [komb(i) for i in spr]
        bloki = [set(len(j) for j in i) for i in kombinacije]
        bloki = [i for i in product(*tuple(bloki)) if sum(i) == len(num)] # veljavne kombinacije dolzin
        for blok in bloki:
            kandidati = [{i: v for i, v in k.items() if len(i) == d} for k, d in zip(kombinacije, blok)]
            nnn = [kk for kk in product(*tuple(k for k in kandidati))]
            #nnn = [kk for kk in product(*tuple(k for k in kandidati)) if sum(sum(i) for i in kk) == sum(num)]
            ok += sum(math.prod(kandidati[i][n] for i, n in enumerate(nn)) for nn in nnn if tuple(j for i in nn for j in i) == num)
        p2.append(ok)
        print(p2)
    print(f"A2: {sum(p2)}")

if __name__ == '__main__':
    main()
