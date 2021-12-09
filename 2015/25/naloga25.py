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
    row = 2981
    col = 3075
    
    # row = 6
    # col = 6

    # Part 1
    if True:
        num = pd.Series(range(row+col-1)).cumsum().iloc[-1]+col
        code = 20151125
        for i in range(2, num+1):
            if (i % 10**6) == 0: print(f"{round(i/num,3)} %")
            code = (code * 252533) % 33554393
        print(f"A1: {code}")
          
    
    # Part 2

    print(f"A2: {0}")


if __name__ == '__main__':
    main()
