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
    register = {chr(k): 0 for k in range(ord('a'), ord('h')+1)}
    code = {}
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            ixy = ln.replace('\n', '').split()
            code.update({i: (ixy[0],) + tuple(k if k in register else int(k) for k in ixy[1:])})

    # Part 1
    if True:
        reg = register.copy()
        pos = 0
        p1 = 0
        while pos in code:
            match code[pos]:
                case 'set', x, y:
                    reg[x] = reg.get(y, y)
                case 'sub', x, y:
                    reg[x] -= reg.get(y, y)
                case 'mul', x, y:
                    reg[x] *= reg.get(y, y)
                    p1 += 1
                case 'jnz', x, y:
                    if reg.get(x, x):
                        pos += reg.get(y, y)-1
                case _:
                    raise Exception()
            pos += 1
        print(f"A1: {p1}")

    # Part 2
    def cycle(reg, pos = 0, max_cycle = None):
        nn = 0
        while pos in code:
            nn += 1
            if max_cycle is None or nn <= max_cycle:
                match code[pos]:
                    case 'set', x, y:
                        reg[x] = reg.get(y, y)
                    case 'sub', x, y:
                        reg[x] -= reg.get(y, y)
                    case 'mul', x, y:
                        reg[x] *= reg.get(y, y)
                    case 'jnz', x, y:
                        if reg.get(x, x):
                            pos += reg.get(y, y)-1
                    case _:
                        raise Exception()
                pos += 1
            else:
                break
            if nn % 10**7 == 0: print([i[-1] for i in sorted(reg.items())])
        return reg

    def is_prime(n):
        if n == 2 or n == 3: return True
        if n < 2 or n%2 == 0: return False
        if n < 9: return True
        if n%3 == 0: return False
        r = int(n**0.5)
        f = 5
        while f <= r:
            if n % f == 0: return False
            if n % (f+2) == 0: return False
            f += 6
        return True

    reg = register.copy()
    reg['a'] = 1
    """ ANALYS
    Na zacetku je inicializacija, do pozicije 8 (set f 1).+
        Inicializacija postavi registre če je:
            a enak 0: b in c na 93
            a enak 1: b na 109300 in c na 126300
        V bistvu h na koncu vsebuje število vseh ne-praštevil med b in (vključno) c s korakom 17
    """
    if True: # Manualy
        reg = cycle(reg, max_cycle = 100)
        print(f"A2: {len([i for i in range(reg['b'], reg['c']+1, 17) if not is_prime(i)])}")
    else:  # Simulacija... to bi trajalo zelooooo dolgo...
        reg = cycle(reg)
        print(f"A2: {reg['h']}")

if __name__ == '__main__':
    main()
