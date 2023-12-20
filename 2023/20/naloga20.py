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
    typ = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' -> ')
            if da[0][0] in {'%', '&'}:
                idx = da[0][1:]
                typ.update({idx: da[0][0]})
            else:
                idx = da[0]
            data.update({idx: [i for i in da[1].split(', ')]})


    def sprejem(signals):
        for (source, destination), signal in signals.items():
            stevec[signal] += 1
            hist.append((source, signal, destination))
            if typ.get(destination) == '%':
                if not signal:
                    stanje[destination] = not stanje[destination]
            elif typ.get(destination) == '&':
                stanje[destination][source] = signal

    def oddaja(signals):
        
        def send(sig):
            for mod in submodul:
                nxt.update({(destination, mod): sig})

        nxt = {}
        for(source, destination), signal in signals.items():
            if destination not in data:
                continue
            submodul = data[destination]
            if typ.get(destination) == '%':
                if not signal:
                    send(stanje[destination])
            elif typ.get(destination) == '&':
                if all(stanje[destination].values()):
                    send(False)
                else:
                    send(True)
            elif destination == 'broadcaster':
                send(signal)
        return nxt

    # Part 1
    if True:
        conj_in = {k: {kk for kk, vv in data.items() if k in vv} for k, v in typ.items() if v == '&'}
        stanje =  {k: {kk: False for kk, vv in data.items() if k in vv} for k, v in typ.items() if v == '&'} | {k: False for k, v in typ.items() if v == '%'}
        stevec = {False: 0, True: 0}
        for _ in range(1000):
   #         vhod_ = copy.deepcopy(vhod)
            hist = []  
   #         stevec[False] += 1  # Button
            todo = {('button', 'broadcaster'): False}
            while len(todo) > 0:
                sprejem(todo)
                todo = oddaja(todo)

        print(f"A1: {math.prod(stevec.values())}")

# tt:
# 747761786
# 771937371 too low
# 709473499
# 1668452499 too high

# d
# 642639957 too low
    # Part 2
    #            proces('broadcaster', vhod)
    dat=copy.deepcopy(data)
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
