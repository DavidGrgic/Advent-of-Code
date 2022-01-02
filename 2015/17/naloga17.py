# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import itertools
import mat

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += [int(ln)]

    target = 150 if len(data) > 5 else 25

    state = []
    for i in range(len(data)):
        state += list(itertools.combinations(data, i+1))


    # Part 1
    if True:
        comb = [i for i in state if sum(i) == target]
        print(f"A1: {len(comb)}")


    # Part 2
    num = min(len(i) for i in comb)
    mcomb = [i for i in comb if len(i) == num]
    print(f"A2: {len(mcomb)}")


if __name__ == '__main__':
    main()
