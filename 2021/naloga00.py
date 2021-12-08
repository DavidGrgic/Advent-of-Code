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
    with open('tdata.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                pass
            da = ln.split(',')
            data += [da]


    # Part 1
    if True:

        print(f"A1: {0}")
          
    
    # Part 2

    print(f"A2: {0}")


if __name__ == '__main__':
    main()
