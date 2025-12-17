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
    with open('d.txt', 'r') as file:
        for l, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' ')
            data += [{'l': tuple(i == '#' for i in da[0][1:-1]),
                      'b': [tuple(int(i) for i in b[1:-1].split(',')) for b in da[1:-1]],
                      'j': tuple(int(i) for i in da[-1][1:-1].split(','))}]

    # Part 1
    def process(light, button):
        
        def press(lig, but):
            return tuple(not l if i in but else l for i, l in enumerate(lig))
        
        stanje = {(False,) * len(light)}
        k = 0
        while light not in stanje:
            k += 1
            stanje = {press(s, b) for s in stanje for b in button}
        return k
    
    
    def linsol(joltage, button):
        h = highspy.Highs()
        h.setOptionValue("log_to_console", False)
        h.setOptionValue("log_dev_level", 0)
        h.setOptionValue("mip_rel_gap", 10000)
        h.setOptionValue("mip_abs_gap", 10000)
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

    def get_rng(joltage, button, mng):
        rng = [[0, min(joltage[i] for i in b)] for b in button]  # Button presses is limited so that no light is over-joltage
        while True:
            rng_ = copy.deepcopy(rng)
            for l, but in mng.items():
                for b in but:
                    ut = but - {b}
                    if ut:
                        rng[b][0] = max(rng[b][0], joltage[l] - sum(rng[i][-1] for i in ut))
                        rng[b][1] = min(rng[b][1], joltage[l] - sum(rng[i][0] for i in ut))
                    else:
                        rng[b][0] = max(rng[b][0], joltage[l])
                        rng[b][1] = min(rng[b][1], joltage[l])
            if rng_ == rng:
                break
        return rng


#    def compositions_old(x, n):
#        for cuts in combinations(range(x + n - 1), n - 1):
#            points = (-1,) + cuts + (x + n - 1,)
#            yield tuple(points[i+1] - points[i] - 1 for i in range(n))

    def compositions(x, rn):
        n = len(rn)
        for cuts in combinations(range(x + n - 1), n - 1):
            points = (-1,) + cuts + (x + n - 1,)
            comp = tuple(points[i+1] - points[i] - 1 for i in range(n))
            if not all(rn[i][0] <= c <= rn[i][1] for i, c in enumerate(comp)):
                continue
            yield tuple(points[i+1] - points[i] - 1 for i in range(n))


    if True:
        dat=copy.deepcopy(data)
        p1 = []
        for da in dat:
            p1.append(process(da['l'], da['b']))
        print(f"A1: {sum(p1)}")

    # Part 2
    dat=copy.deepcopy(data)
    p2 = []
    for da in dat:
        joltage = da['j']
        button = da['b']
        mng = {i: {k for k, v in enumerate(button) if i in v} for i in range(len(joltage))}  # Which lights (key) are managed by which buttons (value)
        mng_ = {i[0]: i[1] for i in sorted(mng.items(), key=lambda x: len(x[1]))}
        mng = {(k := next(iter(mng_))): mng_[k]}  # Reorder so that each next managed light is managed by smallest number of additional buttons
        while (m := set(mng)) != (m_ := set(mng_)):
            lst = tuple(mng)[-1]
            nxt = sorted(((i, len(mng_[i] - mng_[lst])) for i in m_ - m), key=lambda x: x[1])[0][0]
            mng[nxt] = mng_[nxt]
        rng = get_rng(joltage, button, mng)
        combi = {()}  # All valid button combinations
        index = []  # Button index (position) for valid button combinations
        for l, but in mng.items():
            ix = [i for i in but if i not in index]  # Buttons, to be manipulated to get light l right joltage
            if not ix:
                combi = {com for com in combi if
                          joltage[l] == sum(com[i] for i, v in enumerate(index) if v in but and v not in ix)}
            else:
                combi_ = set()
                for com in combi:
                    c_ = [com[i] for i, v in enumerate(index) if v in but and v not in ix]  # Presses of the buttons, already included in valid combinations
                    if (jol := joltage[l] - sum(c_)) < 0:
                        continue
#                    combi_ |= {com + i for i in compositions_old(jol, len(ix))}

#                    [c for c in compositions(jol, [[0,3], [0,2]])]

                    combi_ |= {com + c for c in compositions(jol, [rng[i] for i in ix])}
                combi = combi_
            index += ix
            print(f"\t({l}): {len(next(iter(combi)))} / {len(combi)}")
        p2.append(min(sum(i) for i in combi))

        print(f"# {len(p2)}: {p2[-1]}\t{linsol(da['j'], da['b'])}")
    print(f"A2: {sum(p2)}")  # 16036, 16049 too low, 16050, 16103

if __name__ == '__main__':
    main()
