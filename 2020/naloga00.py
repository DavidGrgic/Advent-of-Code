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
#    data = pd.read_csv('data.csv', header = None).iloc[:,0].astype(int)
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            ins, val = ln.split(' ')
            data += [(ins, eval(val))]

    # Part 1

    print(data)


    # Part 2

    print(data)

if __name__ == '__main__':
    main()
