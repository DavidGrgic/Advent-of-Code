# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import hashlib

def main():

    # Read
    data = 'abcdef'
    data = 'iwrupvqb'

    # Part 1
    if True:
        i = 0
        while True:
            i += 1
            if hashlib.md5((data + str(i)).encode()).hexdigest()[:5] == '00000':
                break
        print(f"A1: {i}")
          
    
    # Part 2
    i = 0
    while True:
        i += 1
        if hashlib.md5((data + str(i)).encode()).hexdigest()[:6] == '000000':
            break
    print(f"A2: {i}")


if __name__ == '__main__':
    main()
