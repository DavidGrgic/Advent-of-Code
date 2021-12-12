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
            data += [ln]


    # Part 1
    vow = {'a', 'e', 'i', 'o', 'u'}
    bad = {'ab', 'cd', 'pq', 'xy'}
    if True:
        res1 = []
        for ln in data:
            nice = True
            x = [i for i in ln if i in vow]
            if len(x) < 3:
                nice = False
            x = np.array([i for i in ln])
            if not (x[:-1] == x[1:]).any():
                nice = False
            for i in bad:
                if ln.find(i) >= 0:
                    nice = False
            if nice:
                res1 += [ln]
        print(f"A1: {len(res1)}")
          
    
    # Part 2
    res2 = []
    for ln in data:
        nice = True
        pair = False
        for i in range(len(ln)-2):
            pa = ln[i:i+2]
            for j in range(len(ln)-2-i):
                if ln[j+i+2:].find(pa) >= 0:
                    pair = True
                    break
            if pair:
                break
        if not pair:
            nice = False
        x = np.array([i for i in ln])
        if not (x[:-2] == x[2:]).any():
            nice = False
        if nice:
            res2 += [ln]
    print(f"A2: {len(res2)}")


if __name__ == '__main__':
    main()
