# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import math, copy
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
            data = ln.replace('\n', '')

    # Part 1
    if True:
        for i in range(len(data)-4):
            if len(set(data[i:i+4])) == 4:
                break
        print(f"A1: {i+4}")

    # Part 2
    for i in range(len(data)-14):
        if len(set(data[i:i+14])) == 14:
            break
    print(f"A2: {i+14}")

if __name__ == '__main__':
    main()
