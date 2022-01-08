# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    def toint(x):
        try:
            return int(x)
        except:
            return x
    
    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = tuple(toint(i.replace(',', '')) for i in ln.split())
            data += [da]


    def comp(dat, a_init = 0):
        reg = {'a': a_init, 'b': 0}
        i = 0
        while 0 <= i < len(dat):
            if min(reg.values()) < 0:
                raise AssertionError
            if dat[i][0] == 'hlf':
                reg[dat[i][1]] = int(reg[dat[i][1]] / 2)
            elif dat[i][0] == 'tpl':
                reg[dat[i][1]] *= 3
            elif dat[i][0] == 'inc':
                reg[dat[i][1]] += 1
            elif dat[i][0] == 'jmp':
                i += dat[i][1]
                continue
            elif dat[i][0] == 'jie':
                if (reg[dat[i][1]] % 2) == 0:
                    i += dat[i][2]
                    continue
            elif dat[i][0] == 'jio':
                if reg[dat[i][1]] == 1:
                    i += dat[i][2]
                    continue
            else:
                raise AssertionError
            i += 1
        return reg

    # Part 1
    if True:
        res1 = comp(data.copy())
        print(f"A1: {res1['b']}")
          
    
    # Part 2
    res2 = comp(data.copy(), 1)
    print(f"A2: {res2['b']}")


if __name__ == '__main__':
    main()
