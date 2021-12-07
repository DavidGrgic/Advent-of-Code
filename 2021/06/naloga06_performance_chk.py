# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = ln.split(',')
    data = np.array([int(i) for i in data])

    dni = 192
    # Part 1
    dat = data.copy()
    cas1 = [time.time()]
    for i in range(dni):
        nov = dat == 0
        dat[nov] = 7
        dat = np.append(dat,9*np.ones(nov.sum()).astype(int))
        dat -= 1
        cas1 += [time.time()]
    print(f"A1: {dat.shape[0]}")


    # Part 2
    dat = pd.DataFrame([(i,0) for i in data], columns = ['D', 'C']).groupby('D')['C'].count().reindex(range(9), fill_value = 0)
    cas2 =[time.time()]
    for i in range(dni):
        nov = dat.loc[0]
        dat.loc[7] += nov
        dat.loc[9] = nov
        dat.iloc[:-1] = dat.iloc[1:].values
        dat.loc[9] = 0
        cas2 += [time.time()]
    print(f"A2: {dat.sum()}")

    cas = pd.DataFrame([cas1, cas2], index = [1,2], columns = range(dni+1)).T
    for i in cas.columns:
        cas.loc[:,i] -= cas.loc[0,i]
    cas.iloc[1:].round(3).to_csv(__file__.replace('py', 'csv'), sep = ';', decimal = ',', header = False)

if __name__ == '__main__':
    main()
