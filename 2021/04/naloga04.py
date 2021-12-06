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
    ss = None
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if c == 0:
                num = np.array(ln.split(',')).astype(int)
            elif ln == '':
                if ss is not None:
                    data += [np.array(ss)]
                ss = []
            else:
                s = np.array(ln.split()).astype(int)
                ss += [s]
        if ss is not None:
            data += [np.array(ss)]
        data = np.array(data)
                    
    # Part 1
    if True:
        drawn = np.zeros(data.shape).astype(bool)
        for i, n in enumerate(num):
            drawn |= data == n
            res = drawn.all(axis = 1).any(axis = 1) | drawn.all(axis = 2).any(axis = 1)
            if res.any():
                board = np.where(res)[0][0]
                res = data[board,:,:][~drawn[board,:,:]].sum() * n
                break
        print(f"A1: {res}")
          
    
    # Part 2
    drawn = np.zeros(data.shape).astype(bool)
    board = None
    for i, n in enumerate(num):
        drawn |= data == n
        res = drawn.all(axis = 1).any(axis = 1) | drawn.all(axis = 2).any(axis = 1)
        if res.sum() == (data.shape[0]-1):
            board = np.where(~res)[0][0]
        if res.all():
            res = data[board,:,:][~drawn[board,:,:]].sum() * n
            break
    print(f"A2: {res}")


if __name__ == '__main__':
    main()
