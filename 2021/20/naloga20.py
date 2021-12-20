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
    ma = {'.': 0, '#': 1}
    data = []
    sec = 0
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                sec += 1
            elif sec == 0:
                algo = [ma[i] for i in ln]
            elif sec == 1:
                da = [ma[i] for i in ln]
                data += [da]
    data = np.array(data).astype(int)

    b2i = lambda x, M = {v: k for k,v in ma.items()}: '\n'.join(''.join(M[j] for j in i) for i in x)

    # Part 1
    def set_rob(dat, val):
        v = int(val)
        dat[:, [0,-1]] = v
        dat[[0,-1], :] = v

    def expand(dat, rob):
        dat0 = dat.copy()
        dat = np.zeros((dat.shape[0]+2, dat.shape[1]+2)).astype(int)
        dat[(lambda D = dat0: tuple(i+1 for i in np.where(~D)))()] = 0
        dat[(lambda D = dat0: tuple(i+1 for i in np.where(D)))()] = 1
        set_rob(dat, rob)
        return dat

    rob = False
    dat = expand(data.copy(), rob)
    for k in range(2):
        dat = expand(dat, rob)
        dat0 = dat.copy()
        for i in range(1, dat.shape[0]-1):
            for j in range(1, dat.shape[1]-1):
                num = dat0[i-1:i+2,j-1:j+2].reshape(-1)
                num = mat.iter2bin(num)
                dat[i,j] = algo[num]
        rob = not rob
        set_rob(dat, rob)
    dat = dat[1:-1,1:-1]
    print(f"A1: {dat.sum()}")

    # Part 2
    rob = False
    dat = expand(data.copy(), rob)
    for k in range(50):
        dat = expand(dat, rob)
        dat0 = dat.copy()
        for i in range(1, dat.shape[0]-1):
            for j in range(1, dat.shape[1]-1):
                num = dat0[i-1:i+2,j-1:j+2].reshape(-1)
                num = mat.iter2bin(num)
                dat[i,j] = algo[num]
        rob = not rob
        set_rob(dat, rob)
    dat = dat[1:-1,1:-1]
    print(f"A2: {dat.sum()}")


if __name__ == '__main__':
    main()
