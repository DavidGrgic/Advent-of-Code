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
    xyxy = lambda l:  tuple(int(j) for i in l.split(' through ') for j in i.split(','))
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln.find('turn on') == 0:
                da = ('o',) + xyxy(ln[8:])
            elif ln.find('toggle') == 0:
                da = ('x',) + xyxy(ln[7:])
            elif ln.find('turn off') == 0:
                da = ('f',) + xyxy(ln[9:])
            else:
                raise AssertionError()
            data += [da]


    # Part 1
    if True:
        onoff = {'o':True, 'f':False}
        lig = np.zeros((1000,1000)).astype(bool)
        for i in data:
            if i[0] in onoff:
                lig[i[1]:i[3]+1, i[2]:i[4]+1] = onoff[i[0]]
            else:
                lig[i[1]:i[3]+1, i[2]:i[4]+1] = ~lig[i[1]:i[3]+1, i[2]:i[4]+1]
        print(f"A1: {lig.sum()}")
          
    
    # Part 2
    onoff = {'o': 1, 'f': -1, 'x': 2}
    lig = np.zeros((1000,1000)).astype(int)
    for i in data:
        lig[i[1]:i[3]+1, i[2]:i[4]+1] += onoff[i[0]]
        lig[lig < 0] = 0
    print(f"A2: {lig.sum()}")


if __name__ == '__main__':
    main()
