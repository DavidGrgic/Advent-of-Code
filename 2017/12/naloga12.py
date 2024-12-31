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
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            da = ln.replace('\n', '').split(' <-> ')
            data.update({int(da[0]): tuple(int(i) for i in da[1].split(','))})

    # Part 1
    if True:
        net = {0}
        n = 0
        while n < (n := len(net)):
            net |= {j for i in net for j in data[i]}
        print(f"A1: {len(net)}")

    # Part 2
    nets = []
    while len(todo := set(data) - {j for i in nets for j in i}) > 0:
        net_ = {next(iter(todo))}
        n = 0
        while n < (n := len(net_)):
            net_ |= {j for i in net_ for j in data[i]}
        nets.append(net_)
    print(f"A2: {len(nets)}")

if __name__ == '__main__':
    main()
