# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import math
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(',')
            da = [[int(i) for i in d.split('-')] for d in da]
            data += [tuple(set(range(i[0], i[1]+1)) for i in da)]


    # Part 1
    if True:
        r1 = [1 for i in data if len(i[0] | i[1]) == len(i[0]) or len(i[0] | i[1]) == len(i[1])]
        print(f"A1: {sum(r1)}")
          
    
    # Part 2
    r2 = [1 for i in data if len(i[0].intersection(i[1])) > 0]
    print(f"A2: {sum(r2)}")


if __name__ == '__main__':
    main()
