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
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += [int(ln)]


    fuel = lambda x: sum(i//3 - 2 for i in x)
    # Part 1
    if True:
         print(f"A1: {fuel(data)}")
          
    
    # Part 2
    mass = []
    for i in data:
        ma = (i,)
        while True:
            m = max(0, fuel(ma)-sum(ma[1:]))
            if m > 0:
                ma += (m,)
            else:
                break
        mass += [ma]
    fu = [sum(i[1:]) for i in mass]
    print(f"A2: {sum(fu)}")


if __name__ == '__main__':
    main()