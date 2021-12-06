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
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = ln.split(',')
    data = np.array([int(i) for i in data])

    # Part 1
    dat = data.copy()
    if True:
        for i in range(80-1):
            dat -= 1
            nov = dat == 0
            dat[nov] = 7
            dat = np.append(dat,9*np.ones(nov.sum()).astype(int))
        print(f"A1: {dat.shape[0]}")
          
    
    # Part 2
    dat = pd.DataFrame([(i,0) for i in data], columns = ['D', 'C']).groupby('D')['C'].count().reindex(range(9), fill_value = 0)
    for i in range(256):
        nov = dat.loc[0]
        dat.loc[7] += nov
        dat.loc[9] = nov
        dat.iloc[:-1] = dat.iloc[1:].values
        dat.loc[9] = 0
    print(f"A2: {dat.sum()}")


if __name__ == '__main__':
    main()
