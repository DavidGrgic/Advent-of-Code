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
    data = []
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split()
            match da:
                case d if 'new' in d:
                    data.append(('new',))
                case d if 'cut' in d:
                    data.append(('cut', int(da[-1])))
                case d if 'increment' in d:
                    data.append(('inc', int(da[-1])))
                case _:
                    raise ValueError
    no = 10 if len(data) < 72 else 10007

    def new(cc):
        return {i: cc[no-i-1] for i in range(no)}
    
    def cut(cc, n):
        return {i: cc[(i+n) % no] for i in range(no)}
    
    def inc(cc, n):
        return {(i*n) % no: cc[i] for i in range(no)}

    def shuffle(no):
        cards = {i: i for i in range(no)} # key = position, value = card_id
        for i in data:
            match i:
                case ('new',):
                    cards = new(cards)
                case ('cut', n):
                    cards = cut(cards, n)
                case ('inc', n):
                    cards = inc(cards, n)
        return cards

    # Part 1
    if True:
        cards = shuffle(no)
        if len(cards) == 10:
            print('A1: ' + ' '.join(str(i[-1]) for i in sorted(cards.items(), key = lambda item: item[0])))
        else:
            print(f"A1: {next(iter(k for k, v in cards.items() if v == 2019))}")

    def inv_shuffle(dat, kk, no):
        for i in dat[::-1]:
            match i:
                case ('new',):
                    kk = no - kk - 1
                case ('cut', n):
                    kk = (kk + n) % no
                case ('inc', n):
                    kk = (kk * pow(n,-1, no)) % no   # pow(n,-1,no) is the modular inverse of n modulo no
        return kk

    def remove_new(dat, no):
        ret = []
        for i in dat:
            match i:
                case ('new',):
                    ret.extend([('inc', no - 1), ('cut', 1)])
                case _:
                    ret.append(i)
        return ret

    def reduce(dat, no):
        ret = copy.deepcopy(dat)
        pos = 0
        while True:
            match ret[pos], ret[pos+1]:
                case ('cut', x), ('cut', y):
                    ret = ret[:pos] + [('cut', (x + y) % no)] + ret[pos+2:]
                    pos = max(pos-1, 0)
                case ('inc', x), ('inc', y):
                    ret = ret[:pos] + [('inc', (x * y) % no)] + ret[pos+2:]
                    pos = max(pos-1, 0)
                case ('cut', x), ('inc', y):
                    ret = ret[:pos] + [('inc', y), ('cut', (x * y) % no)] + ret[pos+2:]
                    pos = max(pos-1, 0)
                case _:
                    pos += 1
            if pos >= len(ret) - 1:
                break
        return ret

    # Part 2
    no = 119315717514047
    if no == 10:
        print('A2: ' + ' '.join(str(inv_shuffle(data, k, no)) for k in range(no)))
    else:
        nn = 101741582076661
        shuffle_2 = set()
        nn_ = nn
        for k in range(int(math.log(nn) // math.log(2)), -1, -1):
            ostanek = nn_ - 2**k
            if ostanek >= 0:
                shuffle_2 |= {k}
                nn_ = ostanek

        program = {}
        for i in range(max(shuffle_2) + 1):
            program.update({i: reduce(2 * program[i-1] if i-1 in program else remove_new(data, no), no)})

        kk = 2020
        for i in shuffle_2:
            kk = inv_shuffle(program[i], kk, no)
        print(f"A2: {kk}")

if __name__ == '__main__':
    main()
