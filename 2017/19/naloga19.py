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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            data.append(ln.replace('\n', ''))
    assert max(len(i) for i in data) == min(len(i) for i in data)


    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])

    def hike(data):
        collection = ''
        length = 0
        position = (0, data[0].find('|'))
        direction = (1, 0)
        while True:
            length += 1
            position = plus(position, direction)
            match data[position[0]][position[1]]:
                case ' ':
                    break
                case '+':
                    for d in ({(0,1), (0,-1)} if abs(direction[0]) else {(1,0), (-1,0)}):
                        pos = plus(position, d)
                        if pos[0] < len(data) and pos[1] < len(data[0]) and data[pos[0]][pos[1]] not in {' ', '+'}:
                            direction = d
                            break
                case '|' | '-':
                    pass
                case x:
                    collection += x
        return collection, length

    # Part 1
    p1, p2 = hike(data)
    print(f"A1: {p1}")

    # Part 2
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
