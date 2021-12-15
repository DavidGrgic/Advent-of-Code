# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import collections

def main():

    # Read
    ins = {}
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if c == 0:
                poly0 = ln
                continue
            elif ln != '':
                da = ln.split(' -> ')
                ins.update({da[0]: da[1]})


    # Part 1
    if True:
        poly = poly0
        for i in range(10):
            pol = ''
            for k in range(len(poly)-1):
                po = poly[k:k+2]
                p = ins.get(po, '')
                if p == '':
                    print('Error')
                pol += po[0] + p
            poly = pol + poly[-1]
        res1 = collections.Counter(poly)
        res1 = pd.Series(res1).sort_values()
        print(f"A1: {res1.iloc[-1] - res1.iloc[0]}")
          
    
    # Part 2
    poly = {k:0 for k in ins}
    ii = {k: (k[0] + v, v + k[1]) for k, v in ins.items()}
    for k in range(len(poly0)-1):
        poly[poly0[k:k+2]] += 1
    for i in range(40):
        pol = poly.copy()
        for k, v in pol.items():
            p0 = ii[k][0]
            p1 = ii[k][1]
            poly[k] -= v
            poly[p0] += v
            poly[p1] += v
    res2 = [(k[0], v) for k, v in poly.items()]
    res2 = pd.DataFrame(res2, columns = ['C', 'S']).groupby('C')['S'].sum()
    res2.loc[poly0[-1]] += 1
    res2 = res2.sort_values()
    print(f"A2: {res2.iloc[-1] - res2.iloc[0]}")


if __name__ == '__main__':
    main()
