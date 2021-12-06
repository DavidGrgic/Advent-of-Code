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
            if ln == '': # Nov blok podatkov
                pass
            da = [i.split(',') for i in ln.split(' -> ')]
            da = [int(j) for i in da for j in i]
            data += [da]
    data = np.array(data)
    zem = np.zeros((data.max()+1, data.max()+1)).astype(int)


    # Part 1
    K = (data[:,0] == data[:,2]) | (data[:,1] == data[:,3])
    p1 = data[K,:].copy()
    for i in p1:
        if i[0] == i[2]:
            for j in range(i[[1,3]].min(), i[[1,3]].max()+1):
                zem[j,i[0]] += 1
        elif i[1] == i[3]:
            for j in range(i[[0,2]].min(), i[[0,2]].max()+1):
                zem[i[1],j] += 1
    res1 = (zem >= 2).sum()
    print(f"A1: {res1}")


    # Part 2
    p2 = data[~K,:].copy()
    for ii in p2:
        i = ii.copy()
        if i[3] < i[1]:
            i = np.array([i[2],i[3],i[0],i[1]])
        if i[2] < i[0]:
            for p, j in enumerate(range(i[[0,2]].min(), i[[0,2]].max()+1)):
                zem[i[3]-p,j] += 1
        else:
            for p, j in enumerate(range(i[[0,2]].min(), i[[0,2]].max()+1)):
                zem[i[1]+p,j] += 1
    res2 = (zem >= 2).sum()
    print(f"A2: {res2}")


if __name__ == '__main__':
    main()
