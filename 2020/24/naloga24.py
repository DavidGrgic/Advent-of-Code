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
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            k = 0; l = []
            while k < len(ln):
                if ln[k] in {'s', 'n'}:
                    l += [ln[k:k+2]]
                    k += 2
                else:
                    l += [ln[k]]
                    k += 1
            data += [tuple(l)]

    center = tuple([120] * 2)

    hoja = {'e': (0,1), 'se': (1,0), 'sw': (1,-1), 'w': (0,-1), 'nw': (-1,0), 'ne': (-1,1)}

    # Part 1
    flor = pd.np.zeros((center[0]*2, center[1]*2), dtype = int)
    for ln in data:
        point = center
        for i in ln:
            x = hoja[i]
            point = (point[0] + x[0], point[1] + x[1])
        flor[point] = int(not(flor[point]))
    print(flor.sum())
            
    # Part 2
    for dd in range(100):
        flo_ = flor.copy()
        for i in range(flo_.shape[0]):
            for j in range(flo_.shape[1]):
                kk = []
                for k in hoja.values():
                    i_ = i + k[0]
                    j_ = j + k[1]
                    if 0 <= i_ < flo_.shape[0] and 0 <= j_ < flo_.shape[1]:
                        kk += [flo_[i_, j_]]
                kk = sum(kk)
                if flo_[i, j]:
                    if kk == 0 or kk > 2:
                        flor[i, j] = 0
                else:
                    if kk == 2:
                        flor[i, j] = 1
        print('Day={}'.format(dd))
    print(flor.sum())

if __name__ == '__main__':
    main()
