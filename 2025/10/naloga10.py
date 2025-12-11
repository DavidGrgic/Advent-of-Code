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
import highspy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
def plot(data, mapper: dict = {0: '.', 1: '#'}, default: dict = {set: 1, dict: 0}):
    if isinstance(data, set):
        data = {k: default[set] for k in data}
    if isinstance(data, dict):
        offset = tuple(int(min(i[j] for i in data.keys())) for j in range(2))
        img = np.zeros(tuple(int(max(i[j] for i in data.keys())-offset[j])+1 for j in range(2))).astype(int) + default[dict]
        img[tuple(tuple(int(i[j]-offset[j]) for i in data.keys()) for j in range(2))] = list(data.values())
        data = img
    print('\n'+'\n'.join([''.join(mapper.get(i,'?') for i in j) for j in data]))

def main():
    # Read
    data = []
    with open('t.txt', 'r') as file:
        for l, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' ')
            data += [{'l': tuple(i == '#' for i in da[0][1:-1]),
                      'b': sorted([tuple(int(i) for i in b[1:-1].split(',')) for b in da[1:-1]], key=lambda x: len(x)),
                      'j': tuple(int(i) for i in da[-1][1:-1].split(','))}]

    # Part 1
    def process1(light, button):
        
        def press(lig, but):
            return tuple(not l if i in but else l for i, l in enumerate(lig))
        
        stanje = {(False,) * len(light)}
        k = 0
        while light not in stanje:
            k += 1
            stanje = {press(s, b) for s in stanje for b in button}
        return k
    
    def process2(joltage, button):
        
        def press(jol, but):
            return tuple(l+1 if i in but else l for i, l in enumerate(jol))
        
        check = lambda x: all(a <= b for a, b in zip(x, joltage))
        stanje = {(0,) * len(joltage)}
        k = 0
        while joltage not in stanje:
            k += 1
            stanje = {n for s in stanje for b in button if check(n := press(s, b))}
            print(f"\t{k}: {len(stanje)}")
        return k
    
    def linsol(joltage, button):
        h = highspy.Highs()
        h.setOptionValue("log_to_console", False)
        h.setOptionValue("log_dev_level", 0)
        h.setOptionValue("mip_rel_gap", 0)
        h.setOptionValue("mip_abs_gap", 0)
        for i, _ in enumerate(button):
            h.addVar(0, highspy.kHighsInf)
            h.changeColCost(i, 1)
        h.changeColsIntegrality((len_ := len(button)), list(range(len_)),
                                [highspy.HighsVarType.kInteger] * len_)
        for j, l in enumerate(joltage):
            idx = [i for i, b in enumerate(button) if j in b]
            val = (1,) * (len_ := len(idx))
            h.addRow(l, l, len_, idx, val)
        h.run()
        if h.getModelStatus() != highspy.HighsModelStatus.kOptimal:
            print(h.modelStatusToString(h.getModelStatus()))
            raise Exception()
        solution = [int(i) for i in h.getSolution().col_value]
        return sum(solution)
                
    
    def process3(joltage, button):
        
        rng = [[0, max(joltage)]] * len(button)
        mhg
        while joltage not in stanje:
            k += 1
            stanje = {n for s in stanje for b in button if check(n := press(s, b))}
            print(f"\t{k}: {len(stanje)}")
        return k
    
    if True:
        dat=copy.deepcopy(data)
        p1 = []
        for da in dat:
            p1.append(process1(da['l'], da['b']))
        print(f"A1: {sum(p1)}")

    # Part 2
    dat=copy.deepcopy(data)
    p2 = []
    k=0
    for da in dat:
        p2.append(process3(da['j'], da['b']))
        #p2.append(linsol(da['j'], da['b']))
        #p2.append(process2(da['j'], da['b']))
        print(f"# {(k := k+1)}: {p2[-1]}")
    print(f"A2: {sum(p2)}")  # 16036, 16049 too low

if __name__ == '__main__':
    main()
