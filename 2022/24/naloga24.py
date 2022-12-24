# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
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
    mov = {'^': (-1,0), '<': (0,-1), 'v': (1,0), '>': (0,1), '': (0,0)}
    bliz = {}
    k = -1
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            for i, v in enumerate(ln):
                if v in mov:
                    k += 1
                    bliz.update({k: (c-1, i-1, v)})
    shape = (c-1, i-1)

    N = 3

    plus = lambda x, y: (x[0]+y[0],x[1]+y[1])
    over = lambda xy: (xy[0] % shape[0], xy[1] % shape[1])
    move = lambda xyd: over(plus(xyd[:2], mov[xyd[2]]))

    vse = {(i,j) for i in range(shape[0]) for j in range(shape[1])}
    ss = sum(shape)
    nn = N * ss
    tt = 3 * nn
    if True:
        poti = []
        bli = copy.deepcopy(bliz)
        for t in range(tt):
            _bli = {k: move(v) + (v[2],) for k, v in bli.items()}
            pros = vse - {i[:2] for i in bli.values()}
            _pros = vse - {i[:2] for i in _bli.values()}
            for toc in pros:
                for k in {'', '<', '>', 'v', '^'}:
                    _toc = plus(toc, mov[k])
                    if _toc in _pros and 0 <= _toc[0] < shape[0] and 0 <= _toc[1] < shape[1]:
                        poti.append(((t,)+toc, (t+1,)+_toc))
            bli = _bli

    t = 0
    for i, s_e in enumerate([((0,0), (shape[0]-1,shape[1]-1)), ((shape[0]-1,shape[1]-1), (0,0)), ((1,0), (shape[0]-1,shape[1]-1))]):
        starts = list({(s_e[0], toc) for toc in {i[0] for i in poti if i[0][1:] == s_e[0]} if toc[0] >= t})
        ends = sorted({(toc, (-toc[0],) + s_e[1]) for toc in {i[1] for i in poti if i[1][1:] == s_e[1]} if toc[0] >= t + ss})
        G = nx.DiGraph()
        G.add_edges_from(poti + starts + ends)
        for en in ends:
            try:
                opt = nx.shortest_path(G, s_e[0], en[1])
            except nx.exception.NetworkXNoPath:
                #print(f"To early: {1-en[1][0]}")
                continue
            t = 1-opt[-1][0]
            if i == 0:
                print(f"A1: {t}")
            break
    print(f"A2: {t}")

if __name__ == '__main__':
    main()
