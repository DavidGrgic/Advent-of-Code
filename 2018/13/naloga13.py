# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
from functools import cache   # @cache
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '.', 2: '+', 3: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            data.append(ln.replace('\n', ''))

    def dat(i: int, j: int):
        if 0 <= i < len(data):
            ln = data[i]
        else:
            return ' '
        return ln[j] if 0 <= j < len(ln) else ' '

    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])
    neg = lambda a: tuple(-i for i in a)
    turn = {(1,0): {0: (0,1), 2: (0,-1)},
            (-1,0): {0: (0,-1), 2: (0,1)},
            (0,1): {0: (-1,0), 2: (1,0)},
            (0,-1): {0: (1,0), 2: (-1,0)}}

    add = lambda a: path.add(tuple(sorted(((i,j), a))))
    path = set()
    cart = {}
    switch = set()
    assert len({len(i) for i in data}) == 1, "All lines from input data should have same length."
    for i in range(len(data)):
        for j in range(len(data[0])):
            match dat(i,j):
                case '|' | 'v' | '^':
                    add((i-1,j))
                    add((i+1,j))
                    if dat(i,j) == '^':
                        cart.update({len(cart): [(i,j), (-1,0), 0]})
                    elif dat(i,j) == 'v':
                        cart.update({len(cart): [(i,j), (1,0), 0]})
                case '-' | '<' | '>':
                    add((i,j-1))
                    add((i,j+1))
                    if dat(i,j) == '<':
                        cart.update({len(cart): [(i,j), (0,-1), 0]})
                    elif dat(i,j) == '>':
                        cart.update({len(cart): [(i,j), (0,1), 0]})
                case '/':
                    if dat(i-1,j) in {'|', '+', 'v', '^'} and dat(i,j-1) in {'-', '+', '<', '>'}:
                        add((i-1,j))
                        add((i,j-1))
                    else:
                        add((i+1,j))
                        add((i,j+1))
                case '\\':
                    if dat(i-1,j) in {'|', '+', 'v', '^'} and dat(i,j+1) in {'-', '+', '<', '>'}:
                        add((i-1,j))
                        add((i,j+1))
                    else:
                        add((i+1,j))
                        add((i,j-1))
                case '+':
                    add((i-1,j))
                    add((i+1,j))
                    add((i,j-1))
                    add((i,j+1))
                    switch.add((i,j))
                case ' ':
                    pass
                case _:
                    raise Exception()

    @cache
    def move(ij, di, sw):
        nxt = {pth for pth in path if ij in pth} - {tuple(sorted((ij, plus(ij, neg(di)))))}
        if ij in swt:
            di_ = turn[di].get(sw, di)
            sw = (sw + 1) % 3
            ij_ = plus(ij, di_)
        else:
            assert len(nxt) == 1
            ij_ = next(iter(i for i in nxt.pop() if i !=  ij))
            di_ = plus(ij_, neg(ij))
        return ij_, di_, sw

    # Part 1
    if True:
        car = copy.deepcopy(cart)
        swt = copy.deepcopy(switch)
        crash = False
        while not crash:
            for cr, (ij, di, sw) in sorted(car.items(), key=lambda item: item[-1]):
                ij_, di_, sw_ = move(ij, di, sw)
                if ij_ in {i for i,_,_ in car.values()} - {ij}:
                    crash = True
                    break
                car[cr][0], car[cr][1], car[cr][2] = ij_, di_, sw_
            #_img_print(_dict2img({j:1 for i in path for j in i} | {k:2 for k in swt} | {k:3 for k,_,_ in car.values()}))
        print(f"A1: {','.join(str(k) for k in reversed(ij_))}")

    # Part 2
    car = copy.deepcopy(cart)
    swt = copy.deepcopy(switch)
    while len(car) > 1:
        for cr, (ij, di, sw) in sorted(car.items(), key=lambda item: item[-1]):
            if cr not in car:
                continue
            ij_, di_, sw_ = move(ij, di, sw)
            if ij_ in {i for i,_,_ in car.values()} - {ij}:
                cr_ = next(iter(k for k,(x,_,_) in car.items() if x == ij_))
                del car[cr], car[cr_]
            else:
                car[cr][0], car[cr][1], car[cr][2] = ij_, di_, sw_
        #_img_print(_dict2img({j:1 for i in path for j in i} | {k:2 for k in swt} | {k:3 for k,_,_ in car.values()}))
    print(f"A2: {','.join(str(k) for k in reversed(ij_))}")

if __name__ == '__main__':
    main()
