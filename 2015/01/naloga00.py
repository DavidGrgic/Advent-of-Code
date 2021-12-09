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
            if ln == '': # Nov blok podatkov
                pass
            data += [ln]
    data = ''.join(data)

    # Part 1
    cod = {'(':1, ')':-1}
    if True:
        dat = [cod[i] for i in data]
        print(f"A1: {sum(dat)}")
          
    
    # Part 2
    dat = pd.Series(dat).cumsum() < 0
    dat = np.where(dat)[0] + 1
    print(f"A2: {dat[0]}")


if __name__ == '__main__':
    main()
