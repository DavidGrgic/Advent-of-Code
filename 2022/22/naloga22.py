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
    split = False
    data = []
    ins = []
    k = -1
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                split = True
                continue
            if split:
                i = 0
                while i < len(ln):
                    _i = i
                    while i < len(ln) and ln[i] not in {'L', 'R'}:
                        i += 1
                    ins += [int(ln[_i:i])] + ([ln[i]] if i < len(ln) else [])
                    i += 1
            else:
                k += 1
                for i, v in enumerate(ln):
                    if v == ' ':
                        data.append((k, i, 0))
                    elif v == '.':
                        data.append((k, i, 1))
                    elif v == '#':
                        data.append((k, i, 2))
                    else:
                        raise Exception()
    xM = max(i[0] for i in data)
    yM = max(i[1] for i in data)
    dat = np.zeros((xM+1, yM+1)).astype(int)
    for i in data:
        if i[2] == 0:
            continue
        else:
            dat[i[:2]] = i[2]

    trn = {('E', 'R'): 'S', ('S', 'R'): 'W', ('W', 'R'): 'N', ('N', 'R'): 'E', ('E', 'L'): 'N', ('S', 'L'): 'E', ('W', 'L'): 'S', ('N', 'L'): 'W'}
    mov = {'N': (-1,0), 'E': (0,1), 'S': (1,0), 'W':(0,-1)}
    plus = lambda x, y: (x[0]+y[0], x[1]+y[1])
    def over(pos, smer):
        while (not (0 <= pos[0] < dat.shape[0]) or not (0 <= pos[1] < dat.shape[1])) or dat[pos] == 0:
            if not (0 <= pos[0] < dat.shape[0]) or not (0 <= pos[1] < dat.shape[1]):
                if smer == 'E':
                    pos = (pos[0],0)
                elif smer == 'W':
                    pos = (pos[0], dat.shape[1]-1)
                elif smer == 'S':
                    pos = (0,pos[1])
                elif smer == 'N':
                    pos = (dat.shape[0]-1, pos[1])
            elif dat[pos] == 0:
                pos = plus(pos, mov[smer])
        return pos

    # Part 1
    if True:
        pos = (0, np.where(dat[0,:]==1)[0][0])
        smer = 'E'
        for i in ins:
            if isinstance(i, int):
                for _ in range(i):
                    p = over(plus(pos, mov[smer]), smer)
                    if dat[p] == 1:
                        pos = p
                    elif dat[p] == 2:
                        break
                    elif dat[p] == 0:
                        raise Exception
                    else:
                        raise Exception
            else:
                smer = trn[(smer, i)]
        print(f"A1: {1000 * (pos[0]+1) + 4 * (pos[1]+1) + {'E': 0, 'S':1, 'W':2, 'N':3}[smer]}")

    # Part 2
    dat=copy.deepcopy(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
