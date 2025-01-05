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
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            data = ln.replace('\n', '')
            assert c == 0, "Only one line of input data is expected"

    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])
    direction = {'N': (-1,0), 'E': (0,1), 'S': (1,0), 'W': (0,-1)}

    @cache
    def walk(wlk, xy = None):
        ret = set()
        while wlk[0] != '$':
            match wlk[0]:
                case '^':
                    xy = (0,0)
                case '(':
                    idx = 0
                    depth = 1
                    sub = ['']
                    while depth:
                        idx += 1
                        match wlk[idx]:
                            case '(':
                                depth += 1
                            case ')':
                                depth -= 1
                                if not depth:
                                    break
                            case '|':
                                if depth == 1:
                                    sub.append('')
                                    continue
                        sub[-1] += wlk[idx]
                    for su in sub:
                        ret |= walk(su + wlk[idx+1:], xy)
                    wlk = wlk[idx:]
                case d:
                    ret.add(tuple(sorted((xy, xy := plus(xy, direction[d])))))
            wlk = wlk[1:]
        return ret

    # Part 1
    if True:
        door = walk(data)
        G = nx.Graph()
        G.add_edges_from(list(door))
        room = {j for i in door for j in i}
        p1 = []
        for rom in room:
            p1.append(len(nx.shortest_path(G, (0,0), rom))-1)
        print(f"A1: {max(p1)}")

    # Part 2
    p2 = len([i for i in filter(lambda x: x>= 1000, p1)])
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
