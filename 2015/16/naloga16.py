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
    anal = {}
    with open('mfcsam.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(': ')
            anal.update({da[0]: int(da[1])})
    data = {}
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(': ', 1)
            data.update({int(da[0].split()[1]):{i.split(': ')[0]: int(i.split(': ')[1])  for i in da[1].split(', ')}})


    # Part 1
    if True:
        filt = {}
        for sue, itm in data.items():
            if all(anal[k] == v for k, v in itm.items()):
                filt.update({sue: itm})
        print(f"A1: {next(iter(filt.keys()))}")


    # Part 2
    filt = {}
    for sue, itm in data.items():
        comp = []
        for k, v in itm.items():
            if k in {'cats', 'trees'}:
                comp += [v > anal[k]]
            elif k in {'pomeranians', 'goldfish'}:
                comp += [v < anal[k]]
            else:
                comp += [v == anal[k]]
        if all(comp):
            filt.update({sue: itm})
    print(f"A2: {next(iter(filt.keys()))}")


if __name__ == '__main__':
    main()
