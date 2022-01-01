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
    data = 1
    data = 3113322113

    data = [int(i) for i in str(data)]

    def roll(dat, nn):
        for _ in range(nn):
            da = []
            cif = dat[0]
            cnt = 1
            i = 1
            while i < len(dat):
                if dat[i] == cif:
                    cnt += 1
                else:
                    da += [cnt, cif]
                    cif = dat[i]
                    cnt = 1
                i += 1
            dat = da + [cnt, cif]
        return len(dat)

    # Part 1
    if True:
        res1 = roll(data.copy(), 40)
        print(f"A1: {res1}")
          
    
    # Part 2
    res2 = roll(data.copy(), 50)
    print(f"A2: {res2}")


if __name__ == '__main__':
    main()