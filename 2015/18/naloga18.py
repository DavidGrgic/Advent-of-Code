# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    code = {'.': 0, '#': 1}
    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [code[i] for i in ln]
            data += [da]
    data = np.array(data)

    lig = lambda d, C = {v:k for k, v in code.items()}: '\n'.join(''.join(C[j] for j in i) for i in d)


    # Part 1
    if True:
        dat = data.copy()
        for _ in range(100):
            da = dat.copy()
            for y in range(dat.shape[0]):
                for x in range(dat.shape[1]):
                    sub = da[max(0,y-1):y+2, max(0,x-1):x+2].sum()
                    if da[y,x] == 1 and sub not in {3,4}:
                        dat[y,x] = 0
                    elif da[y,x] == 0 and sub in {3}:
                        dat[y,x] = 1
            #print(lig(dat))
        print(f"A1: {dat.sum()}")


    # Part 2
    dat = data.copy()
    corr = ([0, 0, dat.shape[0]-1, dat.shape[0]-1], [0, dat.shape[1]-1, 0, dat.shape[1]-1])
    dat[corr] = 1
    for _ in range(100):
        da = dat.copy()
        for y in range(dat.shape[0]):
            for x in range(dat.shape[1]):
                sub = da[max(0,y-1):y+2, max(0,x-1):x+2].sum()
                if da[y,x] == 1 and sub not in {3,4}:
                    dat[y,x] = 0
                elif da[y,x] == 0 and sub in {3}:
                    dat[y,x] = 1
        dat[corr] = 1
        #print(lig(dat))
    print(f"A2: {dat.sum()}")


if __name__ == '__main__':
    main()
