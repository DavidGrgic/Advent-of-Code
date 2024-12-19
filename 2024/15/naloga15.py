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
_img_map = {0: '.', 1: '#', 2: 'O', 3: '@', 4: '[', 5: ']'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    wall = set()
    boxx = set()
    move = None
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                move = ''
            if move is None:
                for i, v in enumerate(ln):
                    match v:
                        case '@':
                            robot_ = (c,i)
                        case 'O':
                            boxx.add((c,i))
                        case '#':
                            wall.add((c,i))
            else:
                move += ln

    direct = {'^': (-1,0), '>': (0,1), 'v': (1,0), '<': (0,-1)}
    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])

    # Part 1
    if True:
        box = boxx.copy()
        robot = robot_[:]
        for mov in move:
            dir_ = direct[mov]
            rob_ = plus(robot, dir_)
            if rob_ in wall:
                continue
            if rob_ in box:
                b = rob_
                box_ = {}
                sol = False
                while True:
                    box_ |= {b: (b_ := plus(b, dir_))}
                    if b_ in wall:
                        break
                    elif b_ not in box:
                        sol = True
                        break
                    b = b_
                if sol:
                    box = (box - set(box_)) | set(box_.values())
                else:
                    continue
            robot = rob_
            if False:
                print(mov)
                _img_print(_dict2img({i:1 for i in wall} | {i:2 for i in box} | {robot: 3}))
        print(f"A1: {sum(100*i[0]+i[1] for i in box)}")

    # Part 2
    wall = {(i, 2*j + k) for i,j in wall for k in {0,1}}
    box = {((i, 2*j), (i, 2*j + 1)) for i,j in boxx}
    robot = (robot_[0], 2*robot_[1])

    def push(xx, box):
        xx_ = tuple(plus(i, dir_) for i in xx)
        obstacle = set()
        box_ = {}
        for x in xx_:
            if x in wall:
                return {}
            elif x in {j for i in box for j in i}:
                obstacle |= {next(iter({i for i in box if x in i}))}
        if len(obstacle) == 0:
            box_.update({xx: xx_})
        else:
            for oo in obstacle:
                bb_ = push(oo, box - obstacle)
                if bb_:
                    box_ |= {xx: xx_} | bb_
                else:
                    return {}
        return box_

    for mov in move:
        dir_ = direct[mov]
        box_ = push((robot,), box)
        if box_:
            robot = box_.pop((robot,))[0]
            box = (box - set(box_)) | set(box_.values())
        if False:
            print(mov)
            _img_print(_dict2img({i:1 for i in wall} | {i[0]:4 for i in box} | {i[1]:5 for i in box} | {robot: 3}))
    print(f"A2: {sum(100*i[0][0]+i[0][1] for i in box)}")
    
if __name__ == '__main__':
    main()
