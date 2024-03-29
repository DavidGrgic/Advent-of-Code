﻿# -*- coding: utf-8 -*-
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
    with open('data.txt', 'r') as file:
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
    vel = np.zeros_like(pos)
    pos0 = pos.copy(); vel0 = vel.copy()
    xyz = {}
    k = 0
    while len(xyz) < 3:
        k += 1
        vel += np.array([np.sign(pos[[i for i in range(pos.shape[0]) if i != p],:] - pos[p,:]).sum(axis = 0) for p in range(pos.shape[0])])
        pos += vel
        for i in range(3):
            if i not in xyz:
                if ((pos[:,i] == pos0[:,i]) & (vel[:,i] == vel0[:,i])).all():
                    xyz.update({i: k})
    print(f"A2: {lcm(*xyz.values())}")


if __name__ == '__main__':
    main()
