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
_img_map = {0: ' ', 1: '.', 2: '#', 3: 'x'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main(prod = True):
    # Read
    split = False
    data = []
    ins = []
    k = -1
    with open('d.txt' if prod else 't.txt', 'r') as file:
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

    trn = {('E', 'R'): 'S', ('S', 'R'): 'W', ('W', 'R'): 'N', ('N', 'R'): 'E', ('E', 'L'): 'N', ('S', 'L'): 'E', ('W', 'L'): 'S', ('N', 'L'): 'W'}
    mov = {'N': (-1,0), 'E': (0,1), 'S': (1,0), 'W':(0,-1)}
    plus = lambda x, y: (x[0]+y[0], x[1]+y[1])
    

    xM = max(i[0] for i in data) +1
    yM = max(i[1] for i in data) +1
    # Part 1
    if True:
        dat = np.zeros((xM, yM)).astype(int)
        for i in data:
            if i[2] == 0:
                continue
            else:
                dat[i[:2]] = i[2]

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
                    else:
                        raise Exception
            else:
                smer = trn[(smer, i)]
        print(f"A1: {1000 * (pos[0]+1) + 4 * (pos[1]+1) + {'E': 0, 'S':1, 'W':2, 'N':3}[smer]}")

    # Part 2
    size = abs(yM-xM)
    assert size != 0 and yM % size == 0 and xM % size == 0

    def plot3d(pos):
        img = np.zeros((xM+2, yM+2)).astype(int)
        for plo, frm in dat.items():
            img[1+plo[0]*size:1+(plo[0]+1)*size, 1+plo[1]*size:1+(plo[1]+1)*size] = frm
        img[1+pos[2]*size + pos[0], 1+pos[3]*size + pos[1]] = 3
        _img_print(img)

    ploskev = lambda pos: (pos[0] // size, pos[1] // size)
    dat = {ploskev(i[:2]): np.zeros((size, size)).astype(int) for i in data if i[2] != 0}  # Dovoljeni ploskve, e.g. ploskve na zvitku
    for i in data:
        if i[2] == 0:
            continue
        dat[ploskev(i[:2])][i[0] % size, i[1] % size] = i[2]

    # glue values have new ploskev xy, new direction, bool True if x and y swap, sign when calculating x and sign when calculating y
    #          A                                    B                                    C                                    D                                      E                                      F                                      G
    glue_t = {(0,2, 'W'): (1,1, 'S', True, -1, 1), (1,2, 'E'): (2,3, 'S', True, 1, -1), (1,1, 'S'): (2,2, 'E', True, -1, 1), (1,0, 'S'): (2,2, 'N', False, -1, -1), (0,2, 'E'): (2,3, 'W', False, -1, -1), (0,2, 'N'): (1,0, 'S', False, -1, -1), (1,0, 'W'): (2,3, 'N', True, -1, -1)}
    glue_p = {(1,1, 'W'): (2,0, 'S', True, -1, 1), (2,1, 'S'): (3,0, 'W', True, 1, -1), (0,2, 'S'): (1,1, 'W', True, 1, -1), (0,1, 'W'): (2,0, 'E', False, -1, -1), (0,2, 'E'): (2,1, 'W', False, -1, -1), (0,1, 'N'): (3,0, 'E', True, 1, -1), (0,2, 'N'): (3,0, 'N', False, 1, 1)}
    #          A                                    B                                    C                                    D                                      E                                      F                                    G
    glue = glue_p if prod else glue_t
    oposite = lambda x, D=list(mov): D[ (D.index(x) + 2) % 4]
    glue |= {v[:2] + (oposite(v[2]),): k[:2] + (oposite(k[2]), v[3]) + v[4:][::-1] for k, v in glue.items()}

    pos = (0, min(k for k, i in enumerate(data) if i[0] == 0 and i[2] == 1))
    pos = tuple(i % size for i in pos) + ploskev(pos)
    smer = 'E'
    for i in ins:
        if isinstance(i, int):
            for _ in range(i):
                _p = plus(pos[:2], mov[smer]) + pos[2:]
                _s = smer
                #plot3d(_p)
                if not ((0 <= _p[0] < size) and (0 <= _p[1] < size)):  # Premaknemo se na drugo ploskev
                    plos = plus(_p[2:], mov[smer])                    # Nova plos
                    if plos in dat:
                        _p = tuple(j % size for j in _p[:2]) + plos
                    else:
                        trans = glue[_p[2:] + (smer,)]
                        xy = tuple(i % size for i in _p[:2])[::-1 if trans[3] else 1]
                        xy = tuple((j if s == 1 else size - 1 - j) % size for j, s in zip(xy, trans[-2:]))
                        _p = xy + trans[:2]
                        _s = trans[2]
                if dat[_p[2:]][_p[:2]] == 1:
                    pos = _p
                    smer = _s
                    #plot3d(pos)
                elif dat[_p[2:]][_p[:2]] == 2:
                    break
                else:
                    raise Exception
        else:
            smer = trn[(smer, i)]
    po3d = pos[2]*size + pos[0], pos[3]*size + pos[1]
    print(f"A2: {1000 * (po3d[0]+1) + 4 * (po3d[1]+1) + {'E': 0, 'S':1, 'W':2, 'N':3}[smer]}")

if __name__ == '__main__':
    main(True)
