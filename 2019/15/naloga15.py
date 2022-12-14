# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import networkx as nx
import copy
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
_img_map = {0: '#', 1: ' ', 2: 'O', -1: 's', -5: '.'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    plus = lambda x, y: (x[0]+y[0],x[1]+y[1])    

    def plot(pro):
        offset = tuple(min(min(i[j] for i in pro),0 if j == 1 else 10**10) for j in range(2))
        x = np.zeros(tuple(max(i[j] for i in pro) - offset[j] + 1 for j in range(2))).astype(int)-5
        for k, v in pro.items():
            x[plus(k, (-offset[0],-offset[1]))] = v
        x[plus((0,0), (-offset[0],-offset[1]))] = -1
        _img_print(x.T)    

    def intcode(dat, _input = [], pos = 0, base = 0, no_out = None):
        _output = []
        _consumed = []
        address = lambda p, m: p+base if m == 2 else p
        value = lambda p, m: dat.get(address(dat[p],m), 0) if m in {0,2} else dat.get(p, 0)
        while True:
            ins = str(dat[pos])
            ins = (5-len(ins))*'0' + ins
            mod = [int(i) for i in ins[-3::-1]]
            ins = int(ins[-2:])
            if ins == 99:
                stop = True
                break
            if ins == 1:
                assert mod[2] in {0,2}
                dat[address(dat[pos+3], mod[2])] = value(pos+1, mod[0]) + value(pos+2, mod[1])
                pos += 4
            elif ins == 2:
                assert mod[2] in {0,2}
                dat[address(dat[pos+3], mod[2])] = value(pos+1, mod[0]) * value(pos+2, mod[1])
                pos += 4
            elif ins == 3:
                assert mod[0] in {0,2}
                assert len(_input) > 0
                dat[address(dat[pos+1], mod[0])] = _input[0]
                _consumed += [_input[0]]
                _input = _input[1:]
                pos += 2
            elif ins == 4:
                _output.append(value(pos+1, mod[0]))
                pos += 2
                if no_out is not None and len(_output) >= no_out:
                    stop = False
                    break
            elif ins == 5:
                if value(pos+1, mod[0]) != 0:
                    pos = value(pos+2, mod[1])
                else:
                    pos += 3
            elif ins == 6:
                if value(pos+1, mod[0]) == 0:
                    pos = value(pos+2, mod[1])
                else:
                    pos += 3
            elif ins == 7:
                assert mod[2] in {0,2}
                dat[address(dat[pos+3], mod[2])] = 1 if value(pos+1, mod[0]) < value(pos+2, mod[1]) else 0
                pos += 4
            elif ins == 8:
                assert mod[2] in {0,2}
                dat[address(dat[pos+3], mod[2])] = 1 if value(pos+1, mod[0]) == value(pos+2, mod[1]) else 0
                pos += 4
            elif ins == 9:
                base += value(pos+1, mod[0])
                pos += 2
            else:
                raise AssertionError
        return dat, _output, -1 if stop else pos, base, _consumed

    # Read
    data = {}
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = {k:int(v) for k, v in enumerate(ln.split(','))}

    # Part 1
    if True:
        dat = copy.deepcopy(data); pos = 0; base = 0
        prostor = {(0,0): 1}
        xy = next(iter(prostor))
        mov = {1: (-1,0), 3: (0,-1), 2: (1,0), 4: (0,1)}
        prefered ={1: (3,1,4,2), 3: (2,3,1,4), 2: (4,2,3,1), 4: (1,4,2,3)}
        smer = 1
        skozi_0 = 0
        while True:
            if xy == (0,0):
                skozi_0 += 1
            _xy = plus(xy, mov[smer])
            dat, stat, pos, base, _cons = intcode(dat, [smer], pos, base, 1)
            stat = next(iter(stat))
            prostor.update({_xy: stat})
            if stat != 0:
                xy = _xy
                if skozi_0 >= 5 and 2 in prostor.values():
                    break
            smeri = {k for k, v in mov.items() if plus(xy, mov[k]) not in prostor} # Prefer searching unknown teritory
            if len(smeri) == 0:
                smeri = {k for k, v in mov.items() if prostor.get(plus(xy, mov[k]),-1) != 0}
                if len(smeri) == 4: # Sredi praznega že raziskanega prostora se želimo pomikati v naključno smer
                    smeri = {next(iter(sorted(smeri, key = lambda x: np.random.random())))}
            smer = next(iter(i for i in prefered[smer] if i in smeri))
        plot(prostor)
        hodnik = {k for k, v in prostor.items() if v >= 1}
        graf = {tuple(sorted([k, plus(k, mov[d])])) for k in hodnik for d, m in mov.items() if plus(k, mov[d]) in hodnik}
        G = nx.Graph()
        G.add_edges_from(list(graf))
        oxi = next(iter({k for k, v in prostor.items() if v == 2}))
        p1 = nx.shortest_path(G, (0,0), oxi)
        print(f"A1: {len(p1)-1}")

    # Part 2
    oxi = {oxi}
    k = 0
    while len(oxi) < len(hodnik):
        oxi |= {plus(k, mov[d]) for k in oxi for d, m in mov.items() if plus(k, mov[d]) in hodnik}
        k += 1
    print(f"A2: {k}")

if __name__ == '__main__':
    main()
