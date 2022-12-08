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
    with open('t1.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' => ')
            k, n = da[1].split(' ')
            d = {tuple(int(m) if j == 0 else m for j, m in enumerate(i.split(' '))) for i in da[0].split(', ')}
            data.update({n: (int(k), d)})

    cup = lambda x, y: x // y + (x % y > 0)

    def cons(num, chm):
        nn, dep = data[chm]
        mul = cup(num, nn)
        ostanek.update({chm: ostanek.get(chm, 0) + mul * nn - num})

        ore = 0
        for i in dep:
            poraba = mul * i[0]
            reciklacija = min(poraba, ostanek.get(i[1],0))
            ostanek.update({i[1]: ostanek.get(i[1], 0) - reciklacija})
            potreba = poraba - reciklacija
            if i[1] == 'ORE':
                ore += potreba
            else:
                ore += cons(*i)
        return ore

    ostanek = {}
    # Part 1
    if True:
        p1 = cons(1, 'FUEL')
        print(f"A1: {p1}")
          
    
    # Part 2

    print(f"A2: {0}")


if __name__ == '__main__':
    main()
