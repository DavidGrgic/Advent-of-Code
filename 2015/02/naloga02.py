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
            da = [int(i) for i in ln.split('x')]
            data += [da]
    data = np.array(data).astype(int)


    # Part 1
    if True:
        plos = np.concatenate([data[:,0] * data[:,1], data[:,1] * data[:,2], data[:,0] * data[:,2]]).reshape((3,-1)).T
        plos = np.append(2 * plos, plos.min(axis = 1).reshape(-1,1), axis = 1)
        print(f"A1: {plos.sum()}")
          
    
    # Part 2
    w1 = 2 * np.sort(data, axis = 1)[:,:2].sum(axis = 1)
    w2 = data.prod(axis = 1)
    print(f"A2: {w1.sum() + w2.sum()}")


if __name__ == '__main__':
    main()
