# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
from itertools import permutations, combinations, product
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
    logic = {}
    logic_ = False
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                logic_ = True
                continue
            if logic_:
                dat, res = ln.split(' -> ')
                da = dat.split()
                logic.update({res: (da[1], (da[0], da[-1]))})
            else:
                da = ln.split(': ')
                data.update({da[0]: int(da[1])})

    def proces(logic, data, max_depth = 99): 
        dat = data.copy()
        while len(todo := set(logic) - set(dat)) > 0:
            max_depth -= 1
            if max_depth < 0:
                return {i: None for i in range(len({k for k in dat if k[0] == 'z'}))}
            for wire in todo:
                o, (xx, yy) = next(iter(l for k, l in logic.items() if k == wire))
                if all(i in dat for i in {xx, yy}):
                    x = dat[xx]; y = dat[yy]
                    match o:
                        case 'AND':
                            ret = x and y
                        case 'OR':
                            ret = x or y
                        case 'XOR':
                            ret = int(x != y)
                        case _:
                            raise RuntimeError()
                    dat.update({wire: ret})
        return {i: b[-1] for i, b in enumerate(sorted({k: v for k, v in dat.items() if k[0] == 'z'}.items()))}

    def root(logic, out, depth=None, normalize=False):
        ins = logic[out]
        if depth is not None:
            depth -= 1
        if depth is None or depth >= 0:
            arg = tuple(i if i[0] in {'x', 'y'} else root(logic, i, depth, normalize) for i in ins[1])
        else:
            arg = tuple(i if i[0] in {'x', 'y'} else '_' for i in ins[1]) if normalize else ins[1]
        return ins[0], tuple(sorted(arg, key = lambda x: str(x)))
    
    def rstr(ins):
        return '(' + {'AND': ' & ', 'OR': ' | ', 'XOR': ' ^ '}[ins[0]].join(i if isinstance(i, str) else rstr(i) for i in ins[1]) + ')'

    def make_up(pos):
        if isinstance(pos, str) and pos[0] == 'z':
            pos = int(pos[1:])
        ret = {}
        for p in range(pos):
            if p == 0:
                ret.update({f"~{str(p).rjust(2,'0')}": ('AND', (f"x{str(p).rjust(2,'0')}", f"y{str(p).rjust(2,'0')}"))})
            else:
                ret.update({f"&{str(p).rjust(2,'0')}": ('AND', (f"x{str(p).rjust(2,'0')}", f"y{str(p).rjust(2,'0')}"))})
                ret.update({f"^{str(p).rjust(2,'0')}": ('XOR', (f"x{str(p).rjust(2,'0')}", f"y{str(p).rjust(2,'0')}"))})
                ret.update({f"+{str(p).rjust(2,'0')}": ('AND', (f"~{str(p-1).rjust(2,'0')}", f"^{str(p).rjust(2,'0')}"))})
                ret.update({f"~{str(p).rjust(2,'0')}": ('OR', (f"&{str(p).rjust(2,'0')}", f"+{str(p).rjust(2,'0')}"))})
        ret.update({f"{'z' if pos == 0 else '^'}{str(pos).rjust(2,'0')}": ('XOR', (f"x{str(pos).rjust(2,'0')}", f"y{str(pos).rjust(2,'0')}"))})
        if pos > 0:
            ret.update({f"z{str(pos).rjust(2,'0')}": ('XOR', (f"~{str(pos-1).rjust(2,'0')}", f"^{str(pos).rjust(2,'0')}"))})
        return ret

    def check(logic, pos):
        dat = {k.replace('z', 'x'): 0 for k in output[:-1]} | {k.replace('z', 'y'): 0 for k in output[:-1]}
        res = proces(logic, dat)
        if res.get(pos) != 0:
            return False
        dat[f"x{str(pos).rjust(2,'0')}"] = 1
        res = proces(logic, dat)
        if res.get(pos) != 1:
            return False
        dat[f"y{str(pos).rjust(2,'0')}"] = 1
        res = proces(logic, dat)
        if res.get(pos) != 0:
            return False
        if pos == len(output)-1 and res.get(pos+1) != 1:
            return False
        dat[f"x{str(pos).rjust(2,'0')}"] = 0
        res = proces(logic, dat)
        if res.get(pos) != 1:
            return False
        if pos > 0:
            dat[f"y{str(pos).rjust(2,'0')}"] = 0
            dat[f"x{str(pos-1).rjust(2,'0')}"] = 1
            dat[f"y{str(pos-1).rjust(2,'0')}"] = 1
            res = proces(logic, dat)
            if res.get(pos) != 1:
                return False
        return True

    # Part 1
    if True:
        p1 = proces(logic, data)
        print(f"A1: {sum(v*2**k for k, v in p1.items())}")

    # Part 2
    manual = False; fast = True
    swaped = set()
    if manual and False:
        swp = ('vcf', 'z10')
        logic[swp[0]], logic[swp[1]] = logic[swp[1]], logic[swp[0]]
        swaped |= set(swp)
    output = sorted(i for i in logic.keys() if i[0] == 'z')
    for pos, out in enumerate(output[:-1]):
        if manual:
            if root(logic, out) == root(make_up(pos), out):
                continue
            else:
                print(f"pos: {pos}:\n{rstr(root(logic, out))}\n{rstr(root(make_up(out), out))}")
                if pos == 10:
                    print('###')
                    print(f"{rstr(root(logic, out))}")  # (x10 & y10)   nastopa semo v formuli za z11
                    print(f"{rstr(root(logic, 'z11',1,True))}\n{rstr(root(make_up('z11'), 'z11',1,True))}")  # To je še OK
                    print(f"{rstr(root(logic, 'z11',2,True))}\n{rstr(root(make_up('z11'), 'z11',2,True))}")  # To ni OK, saj nastopa zgoraj navedeni (x10 & y10)
                    print(f"{rstr(root(logic, 'z11',1))}\n{rstr(root(make_up('z11'), 'z11',1))}")  # Izgleda, da je zamenjava z vcf, eventualno tudi sst
                elif pos == 17:
                    diff = [i for i,(a,b) in enumerate(zip(rstr(root(logic, out)), rstr(root(make_up(out), out)))) if a != b]
                    print(rstr(root(make_up(out), out))[diff[0]:])  # Napaka je pred zadnjim členom, moralo bi biti ... ^ (x17 ^ y17)) namesto ... & (x17 ^ y17))
                    print(f"{rstr(root(logic, out,0,True))}\n{rstr(root(make_up(out), out,0,True))}")  # To ni OK
                    print(f"{rstr(root(logic, out,0))}\n{rstr(root(make_up(out), out,0))}")
                    # TODO
                # TODO
                break
        else:
            while not (root(logic, out) == (make_up_pos := root(make_up(pos), out)) if fast and pos < len(output)-2 else check(logic, pos)):  # fast option is not OK for last bit, which is relevant only for overflow, therefore for last bit, we always use slow option
                if pos == 38:
                    break
                for ss, swp in enumerate(combinations(set(logic.keys()) - swaped, 2)):
                    if ss % 1000 == 0: print(f"pos: {pos}\tswp: {ss}/{math.comb(len(set(logic.keys()) - swaped), 2)}")
                    logic_ = logic.copy()
                    logic_[swp[0]], logic_[swp[1]] = logic_[swp[1]], logic_[swp[0]]
                    if (root(logic_, out, 99) == make_up_pos if fast and pos < len(output)-2 else check(logic_, pos)):
                        logic = logic_
                        swaped |= set(swp)
                        break
                print(f"\t{','.join(sorted(swaped))}")
    print(f"A2: {','.join(sorted(swaped))}")

if __name__ == '__main__':
    main()
