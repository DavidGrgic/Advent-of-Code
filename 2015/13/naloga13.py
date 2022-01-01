# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import itertools

def main():

    # Read
    data = {}
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da1 = ln.split(' would ')
            da2 = da1[1].split(' happiness units by sitting next to ')
            if da2[0][:4] == 'gain':
                val = int(da2[0][4:])
            elif da2[0][:4] == 'lose':
                val = -int(da2[0][4:])
            else:
                raise AssertionError()
            data.update({(da1[0], da2[1][:-1]): val})

    osebe = {i for k in data for i in k}
    
    def maxhapp(osebe):
        nn = len(osebe)
        miza = {}
        for miz in itertools.permutations(osebe):
            miza.update({miz: sum(data.get((miz[i], miz[i-1]),0) + data.get((miz[i], miz[(i+1) % nn]),0)  for i in range(nn))})
        return max(miza.values())

    # Part 1
    if True:
        res1 = maxhapp(osebe)
        print(f"A1: {res1}")
          
    
    # Part 2
    res2 = maxhapp(osebe | {'me'})
    print(f"A2: {res2}")


if __name__ == '__main__':
    main()