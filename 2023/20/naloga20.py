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


    def obdelaj(signals):

        def send(sig):
            for mod in submodul:
                stevec[sig] += 1
                hist.append((destination, sig, mod))
                queue.append((destination, mod, sig))

        queue = []
        for(source, destination, signal) in signals:
            if destination not in data:
                continue
            submodul = data[destination]
            if typ.get(destination) == '%':
                if not signal:
                    stanje[destination] = not stanje[destination]
                    send(stanje[destination])
            elif typ.get(destination) == '&':
                stanje[destination][source] = signal
                if all(stanje[destination].values()):
                    send(False)
                else:
                    send(True)
            elif destination == 'broadcaster':
                send(signal)
        return queue

    # Part 1
    if True:
        stanje =  {k: {kk: False for kk, vv in data.items() if k in vv} for k, v in typ.items() if v == '&'} | {k: False for k, v in typ.items() if v == '%'}
        stevec = {False: 0, True: 0}
        for _ in range(1000):
            hist = []
            todo = [('button', 'broadcaster', False)]
            stevec[False] += 1
            while len(todo) > 0:
                todo = obdelaj(todo)
        print(f"A1: {math.prod(stevec.values())}")

    # Part 2
    stanje =  {k: {kk: False for kk, vv in data.items() if k in vv} for k, v in typ.items() if v == '&'} | {k: False for k, v in typ.items() if v == '%'}
    print(f"A2: {0}")

if __name__ == '__main__':
    main()
