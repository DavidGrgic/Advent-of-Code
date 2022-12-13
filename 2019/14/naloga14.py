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
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' => ')
            k, n = da[1].split(' ')
            d = {tuple(int(m) if j == 0 else m for j, m in enumerate(i.split(' '))) for i in da[0].split(', ')}
            data.update({n: (int(k), d)})

    cup = lambda x, y: x // y + (x % y > 0)

    def pth(chm):
        nn, dep = data[chm]
        ore = set()
        for i in dep:
            if i[1] == 'ORE':
                ore |= {((chm,nn,i[0]),(i[1],1,1))}
            else:
                ore |= {((chm,nn,i[0]),)+j for j in  pth(i[1])}
        return ore

    # Part 1
    if True:
        red = ['FUEL', 'ORE']
        delo = pth(red[0])

        surovine = {j[0] for i in delo for j in i}
        depend = {}
        for s in surovine:
            dep = set()
            for dd in delo:
                d = [d[0] for d in dd]
                if s in d:
                    dep |= set(d[d.index(s)+1:])
            depend.update({s: dep})

        red = []
        while len(red) < len(depend):
            red = [k for k, v in depend.items() if all(i in red for i in v) and k not in red] + red
        material = {'FUEL': 1}
        for r in red:
            if r == 'ORE':
                break
            num = material[r]
            nn, dep = data[r]
            mul = cup(num, nn)
            material.update({r: material.get(r,0) - num})
            for i in dep:
                material.update({i[1]: material.get(i[1],0) + mul * i[0]})
        print(f"A1: {material.get('ORE', 0)}")

    # Part 2

    print(f"A2: {0}")


if __name__ == '__main__':
    main()
