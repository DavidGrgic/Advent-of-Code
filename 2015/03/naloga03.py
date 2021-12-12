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
    data = ''.join(data)

    # Part 1
    if True:
        pot = {(0,0):1}
        xy = next(iter(pot))
        for i in data:
            if i == '>':
                xy = (xy[0] + 1, xy[1])
            elif i == '<':
                xy = (xy[0] - 1, xy[1])
            elif i == '^':
                xy = (xy[0], xy[1] + 1)
            elif i == 'v':
                xy = (xy[0], xy[1] - 1)
            pot[xy] = pot.get(xy,0) + 1
        print(f"A1: {len(pot)}")
          
    
    # Part 2
    pot = {(0,0):2}
    for k in range(2):
        xy = (0,0)
        for i in data[k::2]:
            if i == '>':
                xy = (xy[0] + 1, xy[1])
            elif i == '<':
                xy = (xy[0] - 1, xy[1])
            elif i == '^':
                xy = (xy[0], xy[1] + 1)
            elif i == 'v':
                xy = (xy[0], xy[1] - 1)
            pot[xy] = pot.get(xy,0) + 1
    print(f"A2: {len(pot)}")


if __name__ == '__main__':
    main()
