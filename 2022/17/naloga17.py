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
_img_map = {0: '.', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x[::-1]]));
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
            data = ln.replace('\n', '')

    shape = [((0,0), (0,1), (0,2), (0,3)),
             ((1,0), (0,1), (1,1), (2,1), (1,2)),
             ((0,0), (0,1), (0,2), (1,2), (2,2)),
             ((0,0), (1,0), (2,0), (3,0)),
             ((0,0), (0,1), (1,0), (1,1))]

    def principal_period(s):
        i = (s+s).find(s, 1, -1)
        return None if i == -1 else s[:i]

    def padaj(cik):
        move = lambda x, m: tuple((i[0]+m[0], i[1]+m[1])for i in x)
        zadel = lambda x: any(i in sklad for i in x)
        
        sklad = []; visina = -1; diff = ''; bias = None
        k = 0
        m = 0
        for r in range(10**10 if cik is None else cik):
            padajoca = move(shape[k % 5], (visina + 4, 2))
            while True:
                _padajoca = move(padajoca, (0, 1 if data[m % len(data)] == '>' else -1))
                if not zadel(_padajoca) and all(0 <= i[1] <= 6 for i in _padajoca):
                    padajoca = _padajoca
                _padajoca = move(padajoca, (-1, 0))
                m += 1
                if zadel(_padajoca) or any(i[0] < 0 for i in _padajoca):
                    break
                else:
                    padajoca = _padajoca
            sklad += list(padajoca)
            _visina = max(i[0] for i in sklad)
            diff += str(_visina - visina)
            visina = _visina
            sklad = sklad[-128:]
            k += 1
            if cik is None:
                if False and len({i[1] for i in sklad if i[0] >= visina - 1}) == 7:
                    _img_print(_dict2img({k:1 for k in sklad}))
                    continue
                    # tukaj najdemo vzorec, ko so zgornje dve vrstici zapolnjnei, eden od njih je
                    #
                    #     .#.....
                    #     #######
                    #
                    # kar ustreza [(visina, 1), (visina-1,0), (visina-1,1), (visina-1,2), (visina-1,3), (visina-1,4), (visina-1,5), (visina-1,6)]
                if all(i in sklad for i in [(visina, 1), (visina-1,0), (visina-1,1), (visina-1,2), (visina-1,3), (visina-1,4), (visina-1,5), (visina-1,6)]) and bias is None:
                    bias = r
                    diff_bias = diff
                    diff = ''
                    _img_print(_dict2img({k:1 for k in sklad}))
                    print(f"bias: {bias}")
                if bias is not None and len(diff) > 50:
                    per = principal_period(diff)
                    if per is not None:
                        cikel = 10**12
                        bias_cik = len(diff_bias)
                        vis = sum(int(i) for i in diff_bias)
                        cikel -= bias_cik
                        freq_cik = len(per)
                        vis += (cikel // freq_cik) * sum(int(i) for i in per)
                        osta_cik = cikel % freq_cik
                        vis += sum(int(i) for i in per[:osta_cik])
                        return vis
        return visina

    # Part 1
    if True:
        p1 = padaj(2022)
        print(f"A1: {p1+1}")

    # Part 2
    p2 = padaj(None)
    print(f"A2: {p2}")

if __name__ == '__main__':
    main()
