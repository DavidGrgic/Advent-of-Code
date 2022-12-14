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
_img_map = {0: ' ', 1: '#', 2: 'o'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():
    # Read
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [tuple(int(j) for j in i.split(',')) for i in ln.split(' -> ')]
            data += [da]

    kor = lambda a, b: (min(a, b), max(a, b) + 1)
    plu = lambda x, y: (x[0] + y[0], x[1] + y[1])

    def prostor(dat):
        pro = {}
        for l in dat:
            for i in range(len(l)-1):
                if l[i][0] == l[i+1][0]:
                    x = l[i][0]
                    for y in range(*kor(l[i][1], l[i+1][1])):
                        pro.update({(x,y):1})
                else:
                    y = l[i][1]
                    for x in range(*kor(l[i][0], l[i+1][0])):
                        pro.update({(x,y):1})
        return pro

    def plot(pro):
        offset = tuple(min(min(i[j] for i in pro),0 if j == 1 else 10**10) for j in range(2))
        x = np.zeros(tuple(max(i[j] for i in pro) - offset[j] + 1 for j in range(2)))
        for k, v in pro.items():
            x[plu(k, (-offset[0],-offset[1]))] = v
        _img_print(x.T)

    # Part 1
    if True:
        pro=copy.deepcopy(prostor(data))
        y_max = max(i[1] for i in pro)
        doit = True
        while doit:
            xy = (500, 0)
            while True:
                if xy[1] > y_max:
                    doit = False
                    break
                if plu(xy, [0,1]) not in pro:
                    xy = plu(xy, [0,1])
                elif plu(xy, [-1,1]) not in pro:
                    xy = plu(xy, [-1,1])
                elif plu(xy, [1,1]) not in pro:
                    xy = plu(xy, [1,1])
                else:
                    pro.update({xy:2})
                    break
        print(f"A1: {len({k for k, v in pro.items() if v == 2})}")
        #plot(pro)

    # Part 2
    pro=copy.deepcopy(prostor(data + [[(500-y_max-10, y_max + 2), (500+y_max+10, y_max + 2)]]))
    doit = True
    while doit:
        xy = (500, 0)
        while True:
            if plu(xy, [0,1]) not in pro:
                xy = plu(xy, [0,1])
            elif plu(xy, [-1,1]) not in pro:
                xy = plu(xy, [-1,1])
            elif plu(xy, [1,1]) not in pro:
                xy = plu(xy, [1,1])
            else:
                pro.update({xy:2})
                break
        if xy == (500,0):
            doit = False            
    print(f"A2: {len({k for k, v in pro.items() if v == 2})}")
    #plot(pro)

if __name__ == '__main__':
    main()
