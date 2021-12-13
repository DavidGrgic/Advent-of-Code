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
    fold = []
    with open('data.txt', 'r') as file:
        xy = True
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                xy = False
                continue
            if xy:
                da = [int(i) for i in ln.split(',')]
                data += [da]
            else:
                da = ln[11:].split('=')
                da = [str(da[0]), int(da[1])]
                fold += [da]
    data = np.array(data)


    # Part 1
    if True:
        dat = np.zeros((max(data[:,1])+1, max(data[:,0])+1)).astype(int)
        dat[(data[:,1], data[:,0])] = 1
        for k, i in enumerate(fold):
            if i[0] == 'x':
                le = dat[:, :i[1]]
                de = np.flip(dat[:, i[1]+1:], axis = 1)
                dat = ((le + de) >= 1).astype(int)
            if i[0] == 'y':
                up = dat[:i[1], :]
                dw = np.flip(dat[i[1]+1:, :], axis = 0)
                dat = ((up + dw) >= 1).astype(int)
            if k == 0:print(f"A1: {dat.sum()}")


    # Part 2
    bit2fig = lambda d: '\n'.join([''.join([{0:' ',  1: '#'}[j] for j in i]) for i in d])
    print(f"A2:\n{bit2fig(dat)}")


if __name__ == '__main__':
    main()
