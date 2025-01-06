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
_img_map = {0: '#', 1: '~', 2: '|', 9: '+'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'.') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int) -1
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def main():
    # Read
    clay = set()
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            da = {}
            for l in ln.replace('\n', '').split(', '):
                k, v = l.split('=')
                v = v.split('..')
                da.update({k: (int(v[0]),) if len(v) == 1 else range(*tuple(int(j)+(1 if i else 0) for i,j in enumerate(v)))})
            clay.add(tuple(da[k] for k in ('y','x')))

    plus = lambda a, b: (a[0]+b[0], a[1]+b[1])

    spring = (0, 500)
    # keys: y,x
    # values: clay: 0, still (rest) water: 1, liquid water: 2, spring: 9
    ground = {(y,x): 0 for v in clay for y in v[0] for x in v[1]} | {spring: 9}
    ym = min(y for (y,_),v in ground.items() if v == 0)
    yM = max(y for (y,_),v in ground.items() if v == 0)

    # Part 1
    if True:
        grnd = ground.copy()
        grnd_ = {}
        while grnd_ != (grnd_ := grnd.copy()):
            # Flow of liquid water
            n_ = 0
            while n_ != (n_ := len(grnd)):
                grnd |= {plus((y,x), (1,0)): 2 for (y,x),v in grnd.items() if v >= 2 and y <= yM and plus((y,x), (1,0)) not in grnd}  # Flowing down
                grnd |= {plus(yx, d): 2 for yx,v in grnd.items() for d in {(0,-1), (0,1)} if v >= 2 and plus(yx, d) not in grnd and all(grnd.get(plus(yx, (1,0)), 99) <= 1 for yx_ in {yx, plus(yx, d)})}  # Flowing left/right
            # Liquid water to rest water
            pass
            liquid = sorted({yx for yx, v in grnd.items() if v == 2})
            idx = [0] + [i for i in range(1, len(liquid)) if liquid[i-1][0] != liquid[i][0] or (liquid[i-1][1] + 1 != liquid[i][1])] + [len(liquid)]
            for liq in (liquid[idx[i-1]:idx[i]] for i in range(len(idx)-1,0,-1)):
                if all(grnd.get(plus(yx, (1,0)),72) <= 1 for yx in liq) and grnd.get(plus(liq[0], (0,-1)), 72) <= 0 and grnd.get(plus(liq[-1], (0,1)), 72) <= 0:
                    grnd.update({yx: 1 for yx in liq})
        #_img_print(_dict2img(grnd))
        p1 = {(y,x) for (y,x), v in grnd.items() if ym <= y <= yM and v in {1,2}}
        print(f"A1: {len(p1)}")

    # Part 2
    p2 = {(y,x) for (y,x), v in grnd.items() if ym <= y <= yM and v == 1}
    print(f"A2: {len(p2)}")

if __name__ == '__main__':
    main()
