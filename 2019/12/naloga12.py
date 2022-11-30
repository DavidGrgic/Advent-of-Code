# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
from math import lcm
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    # Read
    data = []
    with open('tdata.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')[1:-1]
            da = ln.split(', ')
            data += [[int(i[2:]) for i in da]]


    pos = np.array(data)
    vel = np.zeros_like(pos)
    # Part 1
    if True:
        for i in range(1,1+1000):
            for p in range(pos.shape[0]):
                vel[p,:] += np.sign(pos[[i for i in range(pos.shape[0]) if i != p],:] - pos[p,:]).sum(axis = 0)
            pos += vel
        print(f"A1: {(abs(pos).sum(axis=1) * abs(vel).sum(axis=1)).sum()}")


    # Part 2
    pos = np.array(data)
    pos = pos.reshape((1,)+pos.shape)
    vel = np.zeros_like(pos)
    ve = {}; po = {}
    k = 0
    while k < 2780:
        k += 1
        vel = np.insert(vel, k, vel[k-1,:,:] + np.array([np.sign(pos[k-1,[i for i in range(pos.shape[1]) if i != p],:] - pos[k-1,p,:]).sum(axis = 0) for p in range(pos.shape[1])]), axis = 0)
        pos = np.insert(pos, k, pos[k-1,:,:] + vel[k,:,:], axis = 0)
        tmp = np.where((pos[k,:,:] == pos[:k,:,:]).all(axis=(1,2)))[0]
        if tmp.shape[0] > 0:
            tmp = sorted(tmp) + [k]
            po.update({tmp[0]: tuple(tmp[1:])})
        tmp = np.where((vel[k,:,:] == vel[:k,:,:]).all(axis=(1,2)))[0]
        if tmp.shape[0] > 0:
            tmp = sorted(tmp) + [k]
            ve.update({tmp[0]: tuple(tmp[1:])})
    po = {i[0]:i[1] for i in sorted(po.items())}
    ve = {i[0]:i[1] for i in sorted(ve.items())}
    print(f"A2: {0}")


if __name__ == '__main__':
    main()
