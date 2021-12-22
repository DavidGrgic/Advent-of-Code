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
            dat = ln.split(' ')
            da = tuple(tuple(int(j) for j in i[2:].split('..')) for i in dat[1].split(','))
            data += [{da: {'off':0 ,'on':1}[dat[0]]}]


    # Part 1
    if True:
        of = 50
        space = np.zeros((2*of+1,2*of+1,2*of+1)).astype(int)
        for i in data:
            k, v = next(iter(i.items()))
            kk = tuple(tuple(i+of for i in j) for j in k)
            space[max(kk[0][0],0):kk[0][1]+1,max(kk[1][0],0):kk[1][1]+1,max(kk[2][0],0):kk[2][1]+1] = v
        print(f"A1: {space.sum()}")


    # Part 2
    sumc = lambda c: mat.prod([i[1]-i[0]+1 for i in c])

    subcub = []  # Vklopljeni subcubi
    for k, dat in enumerate(data):
        #if k % 10 == 0: print(f"{k}/{len(data)}: {len(subcub)}")
        kk, v = next(iter(dat.items()))
        cub = [kk] if v == 1 else []
        for sub in subcub:  #Vse vklopljene subcube popravimo glede na nov cube
            x0 = ((sub[0][0], min(sub[0][1], kk[0][0]-1)), sub[1], sub[2])
            x1 = ((max(sub[0][0], kk[0][1]+1), sub[0][1]), sub[1], sub[2])
            y0 = ((max(sub[0][0], kk[0][0]), min(sub[0][1], kk[0][1])), (sub[1][0], min(sub[1][1], kk[1][0]-1)), sub[2])
            y1 = ((max(sub[0][0], kk[0][0]), min(sub[0][1], kk[0][1])), (max(sub[1][0], kk[1][1]+1), sub[1][1]), sub[2])
            z0 = ((max(sub[0][0], kk[0][0]), min(sub[0][1], kk[0][1])), (max(sub[1][0], kk[1][0]), min(sub[1][1], kk[1][1])), (sub[2][0], min(sub[2][1], kk[2][0]-1)))
            z1 = ((max(sub[0][0], kk[0][0]), min(sub[0][1], kk[0][1])), (max(sub[1][0], kk[1][0]), min(sub[1][1], kk[1][1])), (max(sub[2][0], kk[2][1]+1), sub[2][1]))
            su = [x0,x1,y0,y1,z0,z1]
            su = [s for s in su if all(i[0] <= i[1] for i in s)]
            cub += su
        subcub = cub
    res2 = sum((lambda C = subcub, S = sumc: [S(s) for s in C])())
    print(f"A2: {res2}")


if __name__ == '__main__':
    main()
