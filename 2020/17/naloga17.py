# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():
    
    # Read
#    data = pd.read_csv('data.csv', header = None).iloc[:,0].astype(int)
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            val = [1 if i == '#' else 0 for i in ln.replace('\n','')]
            data += [(val)]

    # Part 1
    dd = pd.np.array(data)
    off = 6+1
    ddd = pd.np.array([[[0 for i in range(dd.shape[1]+2*off)] for j in range(dd.shape[0]+2*off)] for k in range(2*off)])
    ddd[off, off:off + dd.shape[0], off:off + dd.shape[0]] = dd
    d3 = ddd.copy()
    for k in range(6):
        d3_ = d3.copy()
        for i in range(d3_.shape[0]):
            for j in range(d3_.shape[1]):
                for l in range(d3_.shape[2]):
                    oko = d3_[max(i-1,0):i+2, max(j-1,0):j+2, max(l-1,0):l+2]
                    o1 = d3_[i, j, l]
                    n1 = oko.sum()
                    if o1 == 1:
                        if (3 <= n1 <= 4):
                            d3[i, j, l] = 1
                        else:
                            d3[i, j, l] = 0
                    if o1 == 0:
                        if n1 == 3:
                            d3[i, j, l] = 1
                        else:
                            d3[i, j, l] = 0
    print(d3.sum())


    # Part 2
    dd = pd.np.array(data)
    off = 6+1
    dddd = pd.np.array([[[[0 for i in range(dd.shape[1]+2*off)] for j in range(dd.shape[0]+2*off)] for k in range(2*off)] for l in range(2*off)])
    dddd[off, off, off:off + dd.shape[0], off:off + dd.shape[0]] = dd
    d3 = dddd.copy()
    for k in range(6):
        d3_ = d3.copy()
        for i in range(d3_.shape[0]):
            for j in range(d3_.shape[1]):
                for l in range(d3_.shape[2]):
                    for h in range(d3_.shape[3]):
                        oko = d3_[max(i-1,0):i+2, max(j-1,0):j+2, max(l-1,0):l+2, max(h-1,0):h+2]
                        o1 = d3_[i, j, l, h]
                        n1 = oko.sum()
                        if o1 == 1:
                            if (3 <= n1 <= 4):
                                d3[i, j, l,h] = 1
                            else:
                                d3[i, j, l,h] = 0
                        if o1 == 0:
                            if n1 == 3:
                                d3[i, j, l,h] = 1
                            else:
                                d3[i, j, l,h] = 0
    print(d3.sum())


if __name__ == '__main__':
    main()
