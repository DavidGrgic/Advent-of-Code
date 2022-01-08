# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat


def main():

    # Read
    data = ()
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += (int(ln),)

    data = sorted(data, reverse = True)
    nn = len(data)

    def combine(target, pos = 0):
        res = set()
        for i in range(pos, nn):
            if data[i] > target:
                continue
            elif data[i] == target:
                res |= {(data[i],)}
            else:
                re = combine(target - data[i], i+1)
                res |= {(data[i],) + r for r in re}
        return res

    def small_qe(comb):
        clen = sorted(list({len(c) for c in comb}))[0] # Sorted by parcels
        com = [c for c in comb if len(c) == clen]
        com = sorted(com, key = lambda c: mat.prod(c)) # Sorted by quantum entanglment
        return next(iter(com))

    # Part 1
    if True:
        comb = combine(int(sum(data) / 3))
        res1 = small_qe(comb)
        print(f"A1: {mat.prod(res1)}")

    # Part 2
    comb = combine(int(sum(data) / 4))
    res2 = small_qe(comb)
    print(f"A2: {mat.prod(res2)}")

if __name__ == '__main__':
    main()
