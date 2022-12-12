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

    # def cons(num, chm):
    #     nn, dep = data[chm]
    #     mul = cup(num, nn)
    #     ostanek.update({chm: ostanek.get(chm, 0) + mul * nn - num})

    #     ore = 0
    #     for i in dep:
    #         poraba = mul * i[0]
    #         reciklacija = min(poraba, ostanek.get(i[1],0))
    #         ostanek.update({i[1]: ostanek.get(i[1], 0) - reciklacija})
    #         potreba = poraba - reciklacija
    #         if i[1] == 'ORE':
    #             ore += potreba
    #         else:
    #             ore += cons(*i)
    #     return ore
    # ostanek = {}

    # Part 1
    if True:
        red = ['FUEL', 'ORE']
        delo = pth(red[0])
        for pot in {tuple(j[0] for j in i) for i in delo}:
            if pot == tuple(red):
                continue
            j = 0
            for r in pot:
                if r == red[j]:
                    pass
                elif not r in red[j:]:
                    red.insert(j, r)
                j += 1
        
        print(f"A1: {0}")
          
    
    # Part 2

    print(f"A2: {0}")


if __name__ == '__main__':
    main()
