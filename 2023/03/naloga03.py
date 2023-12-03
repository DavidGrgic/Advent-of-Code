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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += [ln]
    data = np.array([[d for d in da] for da in data])

    # Part 1
    if True:
        numbers = []
        for r, row in enumerate(data):
            num = ''
            for i, v in enumerate(row):
                if v.isdigit():
                    num += v
                else:
                    if len(num) > 0:
                        numbers.append((r, i-len(num), i, int(num)))
                        num = ''  
            if len(num) > 0:
                numbers.append((r, i-len(num), i, int(num)))
        p1 = []
        for num in numbers:
            okolica = data[max(num[0]-1,0):num[0]+2, max(num[1]-1,0):num[2]+1]
            okolica = set(j for i in okolica for j in i)
            okolica = {i for i in okolica if not i.isdigit() and not i == '.'}
            if len(okolica) > 0:
                p1.append(num[3])
        print(f"A1: {sum(p1)}")

    # Part 2
    gear = []
    for i, j in zip(*np.where(data == '*')):
        num = []
        for n in numbers:
            if abs(n[0] - i) <= 1 and n[1]-1 <= j <= n[2]:
                num.append(n[3])
        if len(num) == 2:
            gear.append(num)
    print(f"A2: {sum(math.prod(j for j in i) for i in gear)}")

if __name__ == '__main__':
    main()
