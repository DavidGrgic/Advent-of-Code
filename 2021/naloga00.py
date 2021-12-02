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
            ins = ln.split(' ')
            data += [(ins[0], int(ins[1]))]

    # Part 1

    print(f"A1: {0}")
            
    # Part 2

    print(f"A2: {0}")

if __name__ == '__main__':
    main()
