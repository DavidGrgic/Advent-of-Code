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
    role = {}
    data = []
    dat = False
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                dat = True
                continue
            if dat:
                da = {}
                for v in ln[1:-1].split(','):
                    d = v.split('=')
                    da.update({d[0]: int(d[1])})
                data += [da]
            else:
                da = ln.split('{')
                role.update({da[0]: da[1][:-1]})

    def test(obj, wf = 'in'):
        rol = role[wf]
        while True:
            pos = rol.find(':')
            if pos < 0:
                break
            x = obj['x']; m = obj['m']; a = obj['a']; s = obj['s'];
            nxt = rol[pos+1:].split(',')
            if eval(rol[:pos]):
                if nxt[0] in {'A', ':A'}:
                    return True
                elif nxt[0] in {'R', ':R'}:
                    return False
                else:
                    return test(obj, nxt[0])
            else:
                if len(nxt) == 2:
                    if nxt[-1] == 'A':
                        return True
                    elif nxt[-1] == 'R':
                        return False
                    else:
                        return test(obj, nxt[1])
                else:
                    rol = ','.join(nxt[1:])

    # Part 1
    if True:
        x = test(data[4])
        p1 = {}
        for i, dat in enumerate(data):
            if test(dat):
                su = sum(dat.values())
                p1.update({i: su})            
        print(f"A1: {sum(p1.values())}")

    # Part 2
    dat=copy.deepcopy(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
