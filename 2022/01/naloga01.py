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
    data = []; da = ()
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                data += [da]
                da = ()
                continue
            da += (int(ln),)


    # Part 1
    if True:
        print(f"A1: {max(sum(i) for i in data)}")
          
    
    # Part 2
    print(f"A2: {  sum(sorted((sum(i) for i in data), reverse = True)[:3])   }")


if __name__ == '__main__':
    main()
