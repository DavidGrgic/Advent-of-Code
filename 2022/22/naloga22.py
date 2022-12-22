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
    
    
    
    # osi = {(0,0): (       ), (0,1): (None, 1, 0), (0,2): (       ), (0,3): (       ),
    #        (1,0): (       ), (1,1): (0, 1, None), (1,2): (       ), (0,3): (       ),
    #        (2,0): (       ), (2,1): (None, 1, 0), (2,2): (       ), (2,3): (       ),
    #        (3,0): (       ), (3,1): (       ), (3,2): (       ), (3,3): (       )}

    
    # # kvad: prvi dve stevilki povesta po kateri dimenziji (pazi, 1 pomeni dimenzijo x, torej 0, 2 dimenijo y, torej 1, in 3 dimentzijo z, torej 2) tečejo vrstice in stolpci,
    # #       predznak pa v katero smer. tretji bool pa pove če je po preostali dimenziji to prednja (False) ali pa zadnja (True) stranica
    # ploskve = {(0,0): (1, 2, False), (0,1): (1, 3, True), (0,2): (1, -2, True), (0,3): (1, -3, False),
    #         (1,0): (3, 2, True), (1,1): (3, -1, True), (1,2): (3, -2, False), (0,3): (3, 1, False),
    #         (2,0): (-1, 2, True), (2,1): (-1, -3, True), (2,2): (-1, -2, False), (2,3): (-1, 3, False),
    #         (3,0): (-3, 2, False), (3,1): (-3, 1, True), (3,2): (-3, -2, True), (3,3): (-3, -1, False)}

    # ploskve = {(0,1), (1,0), (1,1), (1,2), (1,3), (2,1)}
    # # prvi dve številki id ekvivalentne ploskve, tretja številka kolikorat jo moramo zasukati levo (za 90° v pozitivni smeri) da pridemo do ekvivalentne ploskve
    # ploskve_map = {(0,0): (       ), (0,1): (1, 1, 0), (0,2): (       ), (0,3): (       ),
    #                (1,0): (1, 0, 0), (1,1): (1, 1, 0), (1,2): (1, 2, 0), (1,3): (1, 3, 0),
    #                (2,0): (       ), (2,1): (2, 1, 0), (2,2): (       ), (2,3): (       ),
    #                (3,0): (       ), (3,1): (       ), (3,2): (       ), (3,3): (       )}

    # def flat_3d(pos):
    #     plos = ploskev(pos)
    #     x = ploskve[plos]





    ploskev = lambda pos: (pos[0] // size, pos[1] // size)
    ploskev_over = lambda :0
    dat = {ploskev(i[:2]): np.zeros((size, size)).astype(int) for i in data if i[2] != 0}  # Dovoljeni ploskve, e.g. ploskve na zvitku
    for i in data:
        if i[2] == 0:
            continue
        dat[ploskev(i[:2])][i[0] % size, i[1] % size] = i[2]

    pos = (0, min(k for k, i in enumerate(data) if i[0] == 0 and i[2] == 1))
    pos = tuple(i % size for i in pos) + ploskev(pos)
    smer = 'E'
    for i in ins:
        if isinstance(i, int):
            for _ in range(i):
                p = plus(pos[:2], mov[smer]) + pos[2:]
                if not ((0 <= p[0] < size) and (0 <= p[1] < size)):
                    plos = plus(p[2:], mov[smer])
                    if plos in dat:
                        p = tuple(j % size for j in p[:2]) + plos
                    else:
                        pass
                if dat[p[2:]][p[:2]] == 1:
                    pos = p
                elif dat[p[2:]][p[:2]] == 2:
                    break
                else:
                    raise Exception
        else:
            smer = trn[(smer, i)]
    print(f"A2: {1000 * (pos[0]+1) + 4 * (pos[1]+1) + {'E': 0, 'S':1, 'W':2, 'N':3}[smer]}")

if __name__ == '__main__':
    main()
