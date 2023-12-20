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
    typ = {}
    with open('t.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' -> ')
            if da[0][0] in {'%', '&'}:
                idx = da[0][1:]
                typ.update({idx: da[0][0]})
            else:
                idx = da[0]
            data.update({idx: [i for i in da[1].split(', ')]})

    def pulz(modul, signal):
        
        def send(mod, sig):
            ppp[sig] += 1
            if typ[mod] == '%':
                vhod[mod] = sig
            elif typ[mod] == '&':
                vhod[mod][modul] = sig
            else:
                raise AssertionError()
        
        submodul = data[modul]
        if typ.get(modul) == '%':
            if not signal:
                stanje[modul] = not stanje[modul]
                for i in submodul:
                    send(i, stanje[modul])
        elif typ.get(modul) == '&':
            print('')
        elif modul == 'broadcaster':
            for i in submodul:
                send(i, signal)
        else:
            raise AssertionError()


    # def pulz(modul, signal):
    #     submodul = data[modul]
    #     if typ.get(modul) == '%':
    #         if not signal:
    #             stanje[modul].append(not stanje[modul][-1])
    #             for i in submodul:
    #                 pulz(i, stanje[modul][-1])
    #     elif typ.get(modul) == '&':
    #         pass
    #     elif modul == 'broadcaster':
    #         for i in submodul:
    #             pulz(i, signal)
    #     else:
    #         raise AssertionError()


    # Part 1
    if True:
        # conj_in = {k: [kk for kk, vv in data.items() if k in vv] for k, v in typ.items() if v == '&'}
        # stanje = {i: [False] if typ.get(i) == '%' else ([[False] * len(conj_in[i])] if typ.get(i) == '&' else []) for i in data}
    #    conj_in = {k: {kk: False for kk, vv in data.items() if k in vv} for k, v in typ.items() if v == '&'}
        vhod = {k: {kk: False for kk, vv in data.items() if k in vv} for k, v in typ.items() if v == '&'} | {k: False for k, v in typ.items() if v == '%'}
        stanje = {i: [False] if typ.get(i) in {'%', '&'} else [] for i in data}
        ppp = {False: 0, True: 0}
        for _ in range(1000):
            for k, v in data.items():
                pulz(k, False if k == 'broadcaster' else stanje[k][-1])
        print(f"A1: {0}")

    # Part 2
    dat=copy.deepcopy(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
