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
    # Data
    data = 640441

    # Part 1
    if True:
        board_ = len(board := '37')
        elf = (0, 1)
        while board_ < data + 10:
            board += str(sum(val := tuple(int(board[i]) for i in elf)))
            board_ = len(board)
            elf = tuple((e+v+1) % board_ for e, v in zip(elf, val))
        print(f"A1: {board[data:data+10]}")

    # Part 2
    board_ = len(board := [3,7])
    elf = (0, 1)
    seq = [int(i) for i in str(data)]
    seq_ = len(seq)
    while True:
        for _ in range(10**6):
            d, m = divmod(sum(val := tuple(board[i] for i in elf)), 10)
            board.extend((d,m) if d else (m,))
            board_ = len(board)
            elf = tuple((e+v+1) % board_ for e, v in zip(elf, val))
        if p2 := [(i, i+seq_) for i in range(board_-seq_+1) if board[i:i+seq_] == seq]:
            break
    print(f"A2: {p2[0][0]}")

if __name__ == '__main__':
    main()
