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
            data = [int(i) for i in ln.split(',')]

    data[1]=12; data[2]=2
    
    def intcode(dat):
        pos = 0
        while True:
            if dat[pos] == 99:
                break
            v = (dat[dat[pos+1]], dat[dat[pos+2]])
            if dat[pos] == 1:
                v = sum(v)
            elif dat[pos] == 2:
                v = mat.prod(v)
            else:
                raise AssertionError
            dat[dat[pos+3]] = v
            pos += 4
        return dat
    
    # Part 1
    if True:
        p1 = intcode(data.copy())
        print(f"A1: {p1[0]}")
          
    
    # Part 2
    t = 19690720
    for n in range(100):
        for v in range(100):
            p2 = intcode(data[:1] + [n, v] + data[3:])
            if p2[0] == t:
                break
        if p2[0] == t:
            break
    print(f"A2: {100*n+v}")


if __name__ == '__main__':
    main()
