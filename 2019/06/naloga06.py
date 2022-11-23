# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
from collections import Counter
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = tuple(ln.split(')'))
            data += [da]

    top = {j for i in data for j in i}
    top = {k: {i[1] for i in data if i[0] == k} for k in top}

    def fork(parent):
        if len(top[parent]) == 0:
            return [()]
        else:
            res = []
            for i in top[parent]:
                for j in fork(i):
                    res.append((i,) + j)
            return res

    # Part 1
    if True:
        veje = fork('COM')
        orb = {(j,i+1) for k in veje for i, j in enumerate(k)}
        print(f"A1: {sum(i[1] for i in orb)}")

    # Part 2
    you = [i for i in veje if 'YOU' in i][0]
    you = you[:you.index('YOU')]
    san = [i for i in veje if 'SAN' in i][0]
    san = san[:san.index('SAN')]
    presek = set(you).intersection(san)
    print(f"A2: {len(you)+len(san)-2*len(presek)}")


if __name__ == '__main__':
    main()
