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
            data += [ln]


    # Part 1
    if True:
        len_c = [len(i) for i in data]
        sdata = [i[1:-1] for i in data]
        for k, v in {r'\\': '_', r'\"': '_'}.items():
            sdata = [i.replace(k, v) for i in sdata]
        sdat = []
        for da in sdata:
            while True:
                i = da.find(r'\x')
                if i < 0:
                    break
                da = da[:i] + '_' + da[i+4:]
            sdat += [da]
        len_s = [len(i) for i in sdat]
        print(f"A1: {sum(len_c)-sum(len_s)}")
          
    
    # Part 2
    sdata = data.copy()
    sdata = [i.replace('\\', '\\\\') for i in sdata]
    sdata = [i.replace('\"', '\\\"') for i in sdata]
    len_e = [2+len(i) for i in sdata]
    print(f"A2: {sum(len_e)-sum(len_c)}")


if __name__ == '__main__':
    main()
