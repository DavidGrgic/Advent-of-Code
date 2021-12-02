# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
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
    data = pd.Series(data, dtype = int)


    # Part 1
    chng = data.diff()
    chng = chng.loc[chng.notnull()]
    print(f"A1: {(chng > 0).sum()}")
            
    # Part 2
    smoth = data.rolling(3, min_periods = 3).sum()
    smoth = smoth.diff()
    smoth = smoth.loc[smoth.notnull()]
    print(f"A2: {(smoth > 0).sum()}")
    

if __name__ == '__main__':
    main()
