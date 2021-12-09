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
            da = [int(i) for i in ln]
            data += [da]
    data = np.array(data).astype(int)


    # Part 1
    if True:
        low = np.zeros(data.shape).astype(bool)
        for x in range(data.shape[0]):
            for y in range(data.shape[1]):
                sub = data[max(x-1,0):x+2,max(y-1,0):y+2]
                sub = sub < data[x,y]
                if not sub.any():
                    low[x,y] = True
        res1 = data[low].sum() + low.sum()
        print(f"A1: {res1}")
          
    
    # Part 2
    XY = np.where(low)
    basin = []
    for z in range(low.sum()):
        bas = [(XY[0][z],XY[1][z])]
        i = 0
        while i < len(bas):
            xy = bas[i]
            for ij in [(-1,0), (1,0), (0,-1), (0,1)]:
                x = xy[0] + ij[0]
                y = xy[1] + ij[1]
                if x < 0 or x > data.shape[0]-1 or y < 0 or y > data.shape[1]-1:
                    continue
                if data[x,y] != 9 and (x,y) not in bas:
                    bas += [(x,y)]
            i += 1
        basin += [len(bas)]
    basin.sort()
    res2 = mat.prod(basin[-3:])
    print(f"A2: {res2}")


if __name__ == '__main__':
    main()
