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
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                pass
            da = ln.split(',')
    data = np.array([int(i) for i in da])

    # Part 1
    if True:
        dat = data * np.ones((data.max()+1,1)).astype(int)
        for i in range(dat.shape[0]):
            dat[i,:] = abs(dat[i,:] - i-1)
        dat = dat.sum(axis = 1)
        res = dat[np.where(dat == dat.min())[0][0]]
        print(f"A1: {res}")
          
    
    # Part 2
    dat = data * np.ones((data.max()+1,1)).astype(int)
    cost = pd.Series([i for i in range(dat.shape[0]+1)]).cumsum().to_dict()
    for i in range(dat.shape[0]):
        mov = abs(dat[i,:] - i-1)
        for j in range(mov.shape[0]):
            mov[j] = cost[mov[j]]
        dat[i,:] = mov
    dat = dat.sum(axis = 1)
    res = dat[np.where(dat == dat.min())[0][0]]
    print(f"A2: {res}")


if __name__ == '__main__':
    main()
