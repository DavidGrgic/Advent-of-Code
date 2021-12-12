# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import collections

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split('-')
            data += [da]
    data = np.array(data)

    cave = {}
    for cc in np.unique(data):
        big = cc.isupper()# or cc in {'start', 'end'}
        con = np.append(data[data[:,0] == cc,1], data[data[:,1] == cc,0])
        cave.update({str(cc): (big, {str(i) for i in con})})


    # Part 1
    def pot1(pt):
        cav = pt[-1]
        if cav == 'end':
            return [['end']]
        ppp = []
        for nasl in cave[cav][1]:
            if nasl == 'start':
                continue
            if not cave[nasl][0] and nasl in pt:
                 continue
            pp = pot1(pt + [nasl])
            ppp += [[cav] + k for k in pp]
        return ppp

    if True:
        poti = pot1(['start'])
        print(f"A1: {len(poti)}")


    # Part 2
    def pot2(pt):
        cav = pt[-1]
        if cav == 'end':
            return [['end']]
        ppp = []
        for nasl in cave[cav][1]:
            if nasl == 'start':
                continue
            if not cave[nasl][0] and nasl != 'end': # small and not end
                x = [i for i in pt if not cave[i][0]] + [nasl]
                x = collections.Counter(x).values()
                if sum(x) > len(x) + 1:
                     continue
            pp = pot2(pt + [nasl])
            ppp += [[cav] + k for k in pp]
        return ppp

    poti = pot2(['start'])
    print(f"A2: {len(poti)}")


if __name__ == '__main__':
    main()
