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
            l = []
            for i in ln:
                l += [int(i)]
            data += [l]
                

    # Part 1
    def p1(dat, most_common = True):
        da = np.array(dat).sum(axis = 0)
        da = da > len(dat)/2
        da = da if most_common else np.array([not i for i in da])
        return mat.iter2bin(da.astype(int))
    
    gamma = p1(data, True)
    epsilon = p1(data, False)
    print(f"A1: {gamma*epsilon}")


    # Part 2
    def p2(dat, most_common = True):
        da = np.array(dat).copy()
        for i in range(da.shape[1]):
            t = da[:,i].sum() >= da.shape[0]/2
            t = t if most_common else not t
            t = da[:,i] == int(t)
            da = da[t,:]
            if da.shape[0] == 1:
                break
        return mat.iter2bin(da[0])
    
    oxy = p2(data, True)
    co2 = p2(data, False)
    print(f"A2: {oxy*co2}")


if __name__ == '__main__':
    main()
