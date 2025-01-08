# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#from functools import cache   # @cache
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: '.', 1: 'E', -1: 'G'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'#') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)-72
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    data = {}  # 0: empty space, -G: ID of tht goblin, +E: ID of the elf
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            for j, v in enumerate(ln.replace('\n', '')):
                match v:
                    case '.':
                        data.update({(i,j): 0})
                    case 'G':
                        data.update({(i,j): min((data | {None:0}).values())-1})
                    case 'E':
                        data.update({(i,j): max((data | {None:0}).values())+1})
                    case '#':
                        pass
                    case _:
                        raise Exception()
    unit = {v: 200 for v in data.values() if v != 0}

    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])

    def war(fld, uni, attack = 3, show = False):
        rund = 0; end = False
        while not end:
            for u, xy in enumerate(todo := sorted(ij for ij,v in fld.items() if v != 0)):
                if fld[xy] == 0:  # Unit already killed, skip it
                    continue
                # Move
                start = {plus(xy,d) for d in {(-1,0), (0,-1), (0,1), (1,0)} if fld.get(plus(xy,d), 72) == 0}
                neighbour = sorted(plus(xy,d) for d in {(-1,0), (0,-1), (0,1), (1,0)} if fld.get(xy, 0) * fld.get(plus(xy,d), 0) < 0)
                if start and not neighbour:
                    graf = nx.Graph()
                    graf.add_edges_from([(xy_, plus(xy_,d)) for xy_, v in fld.items() for d in {(1,0), (0,1)} if v == 0 and fld.get(plus(xy_,d), 72) == 0])
                    reach = {}
                    for xy_enemy in {xy_ for xy_, v in fld.items() if fld.get(xy,0) * v < 0}:
                        for xy_range in {plus(xy_enemy, d) for d in {(-1,0), (0,-1), (0,1), (1,0)} if fld.get(plus(xy_enemy, d), 72) == 0}:
                            r = []
                            for xy_start in start:
                                if xy_start == xy_range:
                                    r.append([xy, xy_range])
                                elif graf.has_node(xy_start) and graf.has_node(xy_range) and nx.has_path(graf, xy_start, xy_range):
                                    r.append([xy] + nx.shortest_path(graf, xy_start, xy_range))
                            if r:
                                reach.update({xy_range: sorted(r, key=lambda x: (len(x),x))[0]})
                    if not reach:
                        continue
                    move = sorted(reach.items(), key=lambda item: (len(item[1]), item[0]))[0][-1]
                    fld[move[1]], fld[move[0]] = fld[move[0]], fld[move[1]]
                    x_y = move[1]
                else:
                    x_y = xy
                # Attack
                neighbour = sorted(plus(x_y,d) for d in {(-1,0), (0,-1), (0,1), (1,0)} if fld.get(x_y,0) * fld.get(plus(x_y,d),0) < 0)
                if neighbour:
                    target = sorted((uni[fld[xy_]], xy_) for xy_ in neighbour)[0]
                    uni[fld[target[-1]]] = (hit := max(0, uni[fld[target[-1]]] - (attack if fld[x_y] > 0 else 3)))
                    if not hit:
                        fld[target[-1]] = 0
                        if not all(sum(uni[v] for ij,v in fld.items() if v != 0 and v*s >= 0) > 0 for s in {1,-1}):
                            end = True
                            if u+1 != len(todo):
                                break
            else:
                rund += 1
            if show:
                print(f"After round {rund}", end='')
                _img_print(_dict2img({k: (1 if v > 0 else -1) if v != 0 else 0 for k, v in fld.items()}))
        return uni, rund

    # Part 1
    if True:
        uni, rund = war(data.copy(), unit.copy())
        print(f"A1: {rund * sum(uni.values())}")

    # Part 2
    attk = {}
    while attk.get('M', (72,))[0] - attk.get('m', (0,))[0] > 1:
        atk = ((attk['m'][0] + attk['M'][0]) // 2 if attk.get('M') else 2*attk['m'][0]) if attk.get('m') else 3
        uni, rund = war(data.copy(), unit.copy(), atk)
        if all(win := [v for k, v in uni.items() if k > 0]):
            attk.update({'M': (atk, rund, win)})
        else:
            attk.update({'m': (atk, rund, win)})
    print(f"A2: {attk['M'][1] * sum(attk['M'][2])}")

if __name__ == '__main__':
    main()
