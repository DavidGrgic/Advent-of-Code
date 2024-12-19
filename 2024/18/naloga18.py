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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += [tuple(int(i) for i in ln.split(','))[::-1]]
    dim = (6 if len(data) <= 25 else 70) + 1
    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])
    
    def graf(dat):
        node = [((i,j), plus((i,j), s)) for i in range(dim) for j in range(dim) for s in {(1,0), (-1,0), (0,1), (0,-1)} if (i,j) not in dat and plus((i,j),s) not in dat and 0 <= plus((i,j),s)[0] < dim and 0 <= plus((i,j),s)[1] < dim]
        ret = nx.DiGraph()
        ret.add_edges_from(node)
        return ret
    
    # Part 1
    tim = 12 if len(data) <= 25 else 1024
    gra = graf(data[:tim])
    p1 = nx.shortest_path(gra, (0,0), (dim-1,dim-1))
    print(f"A1: {len(p1)-1}")

    # Part 2
    lim = [tim, len(data)]
    while lim[1]-lim[0] > 1:
        tm = sum(lim) // 2
        gra = graf(data[:tm])
        if nx.has_path(gra, (0,0), (dim-1,dim-1)):
            lim[0] = tm
        else:
            lim[1] = tm
    print(f"A2: {','.join(str(i) for i in data[lim[1]-1][::-1])}")

if __name__ == '__main__':
    main()
