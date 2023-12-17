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
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
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
            data += [[int(i) for i in ln]]
    data = np.array(data)

    # Part 1
    if True:
        G = nx.DiGraph()  # točka: (i, j, d)
        poti = []  #
        for i in range(data.shape[0]):
            for j in range(data.shape[0]):
                for d in {(1,0), (-1,0), (0,1), (0,-1)}:  # Smer
                    tocka = (i, j, d)
                    for d_ in ({(1,0), (-1,0)} if d[0] == 0 else {(0,1), (0,-1)}): # Nova smer
                        w = 0
                        i_ = i
                        j_ = j
                        for _ in range(3):  # premik
                            i_ += d_[0]
                            j_ += d_[1]
                            if not (0 <= i_ < data.shape[0] and 0 <= j_ < data.shape[1]):
                                continue
                            tocka_ = (i_, j_, d_)
                            w += data[i_, j_]
                            poti.append((tocka, tocka_, w))
        poti += [ ('S', (0,0,(1,0)), 0), ('S', (0,0,(0,1)), 0) ]
        poti += [ ((data.shape[0]-1,data.shape[1]-1,(1,0)), 'E', 0), ((data.shape[0]-1,data.shape[1]-1,(0,1)), 'E', 0) ]
        G.add_weighted_edges_from(poti)

        pot = nx.shortest_path(G, 'S', 'E', 'weight')
        w = 0.
        for k in range(len(pot)-1):
            w_ = [i[2] for i in poti if i[0] == pot[k] and i[1] == pot[k+1]]
            if len(w_) == 1:
                w += w_[0]
            else:
                raise AssertionError
        print(f"A1: {w}")

    # Part 2
    G = nx.DiGraph()  # točka: (i, j, d)
    poti = []  #
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            for d in {(1,0), (-1,0), (0,1), (0,-1)}:  # Smer
                tocka = (i, j, d)
                for d_ in ({(1,0), (-1,0)} if d[0] == 0 else {(0,1), (0,-1)}): # Nova smer
                    w = 0
                    i_ = i
                    j_ = j
                    for _ in range(3):
                        i_ += d_[0]
                        j_ += d_[1]
                        if not (0 <= i_ < data.shape[0] and 0 <= j_ < data.shape[1]):
                            continue
                        w += data[i_, j_]
                    for _ in range(7):  # premik
                        i_ += d_[0]
                        j_ += d_[1]
                        if not (0 <= i_ < data.shape[0] and 0 <= j_ < data.shape[1]):
                            continue
                        tocka_ = (i_, j_, d_)
                        w += data[i_, j_]
                        poti.append((tocka, tocka_, w))
    poti += [ ('S', (0,0,(1,0)), 0), ('S', (0,0,(0,1)), 0) ]
    poti += [ ((data.shape[0]-1,data.shape[1]-1,(1,0)), 'E', 0), ((data.shape[0]-1,data.shape[1]-1,(0,1)), 'E', 0) ]
    G.add_weighted_edges_from(poti)

    pot = nx.shortest_path(G, 'S', 'E', 'weight')
    w = 0.
    for k in range(len(pot)-1):
        w_ = [i[2] for i in poti if i[0] == pot[k] and i[1] == pot[k+1]]
        if len(w_) == 1:
            w += w_[0]
        else:
            raise AssertionError
    print(f"A2: {w}")

if __name__ == '__main__':
    main()
