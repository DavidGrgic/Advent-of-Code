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
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [int(i) for i in ln]
            data += [da]
    data0 = np.array(data).astype(int)

    # Part 1
    data = data0.copy()
    flash = 0
    if True:
        for i in range(100):
            data += 1
            fls = np.zeros_like(data).astype(bool)
            while True:
                dat = np.where((data >= 10) & ~fls)
                f = dat[0].shape[0]
                if f == 0:
                    flash += fls.sum()
                    data[fls] = 0
                    break
                for j in range(f):
                    x = dat[0][j]
                    y = dat[1][j]
                    data[max(x-1,0):x+2, max(y-1,0):y+2] += 1
                    fls[dat] = True
        print(f"A1: {flash}")
          
    
    # Part 2
    data = data0.copy()
    i = 0
    while True:
        if i%1000 == 0: print(i)
        i += 1
        data += 1
        fls = np.zeros_like(data).astype(bool)
        while True:
            dat = np.where((data >= 10) & ~fls)
            f = dat[0].shape[0]
            if f == 0:
                flash += fls.sum()
                data[fls] = 0
                break
            for j in range(f):
                x = dat[0][j]
                y = dat[1][j]
                data[max(x-1,0):x+2, max(y-1,0):y+2] += 1
                fls[dat] = True
        if fls.all():
            break
    print(f"A2: {i}")


if __name__ == '__main__':
    main()