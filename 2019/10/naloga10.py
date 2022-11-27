# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    # Read
    data = set()
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            for i, v in enumerate(ln.replace('\n', '')):
                if v == '#':
                    data |= {(c,i)}

    def kot(a, t):  # a: asteroid, kjer smo, t: asteroid tarča
        sig = (1 if t[1] > a[1] else -1) if  t[1] != a[1] else (1 if t[0] > a[0] else -1)
        if t[1] != a[1]:
            x = Fraction(t[0]-a[0],t[1]-a[1])
            x = (x.numerator, sig * x.denominator)
        else:
            x = (sig, 0)
        return x

    def kot4sort(x):
        return (x[1] < 0, x[0]/abs(x[1]) if x[1] != 0 else x[0] * float('inf'))

    def smeri(dat, i):
        res = set()
        dir2tar = {}
        for j in dat:
            if j == i:
                continue
            tmp = kot(i, j)
            res |= {tmp}
            dir2tar.update({j: tmp})
        return res, dir2tar

    # Part 1
    if True:
        p1 = {}
        for i in data:
            p1.update({i: smeri(data, i)[0]})
        print(f"A1: {max(len(i) for i in p1.values())}")

    # Part 2
    base = [k for k, v in sorted(p1.items(), key = lambda x: len(x[1]), reverse = True)][0]
    target = data - {base}
    vap = []
    while len(target) > 0:
        directions, tar_dir = smeri(target, base)
        directions = sorted(directions, key = lambda x: kot4sort(x))
        for d in directions:
            tar = [k for k, v in tar_dir.items() if v == d]
            tar = sorted(tar, key = lambda x: ((x[0]-base[0])**2) + ((x[1]-base[1])**2))
            t = tar[0]
            target -= {t}
            vap.append(t)
    print(f"A2: {vap[199][0] + 100*vap[199][1]}")


if __name__ == '__main__':
    main()
