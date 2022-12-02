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
            da = ln.split(' ')
            data += [tuple(da)]

    card = {'X':1, 'Y':2, 'Z': 3}
    score = {
        ('A', 'X'): 3,
        ('B', 'Y'): 3,
        ('C', 'Z'): 3,
        ('C', 'X'): 6,
        ('B', 'Z'): 6,
        ('A', 'Y'): 6,
        }
    # Part 1
    if True:
        print(f"A1: {sum([score.get(i,0) + card.get(i[1]) for i in data])}")
          
    
    # Part 2
    my_score = {'X':0, 'Y': 3, 'Z': 6}
    my_card = {
        ('A','Y'): 1,
        ('B','Y'): 2,
        ('C','Y'): 3,
        ('A','Z'): 2,
        ('B','Z'): 3,
        ('C','Z'): 1,
        ('A','X'): 3,
        ('B','X'): 1,
        ('C','X'): 2,
        }
    print(f"A2: {sum([(my_card.get(i,0)+ my_score.get(i[1])) for i in data])}")


if __name__ == '__main__':
    main()
