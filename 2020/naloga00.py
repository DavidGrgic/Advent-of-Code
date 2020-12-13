# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd

def main():
    
    # Read
#    data = pd.read_csv('data.csv', header = None).iloc[:,0].astype(int)
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ins, val = ln.split(' ')
            data += [(ins, eval(val))]

    # Part 1

    print(data)


    # Part 2

    print(data)

if __name__ == '__main__':
    main()
