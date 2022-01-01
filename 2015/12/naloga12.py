# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    with open('data.txt', 'r') as file:
        data = file.read()
    data = json.loads(data)


    def usum(dat, omit = None):
        if isinstance(dat, dict):
            if omit is not None and omit in dat.values():
                return 0
            else:
                return sum(usum(i, omit) for i in  dat.values())
        elif isinstance(dat, list):
            return sum(usum(i, omit) for i in  dat)
        elif isinstance(dat, int):
            return dat
        elif isinstance(dat, str):
            return 0
        else:
            raise AssertionError

    # Part 1
    if True:
        res1 = usum(data)
        print(f"A1: {res1}")


    # Part 2
    res2 = usum(data, 'red')
    print(f"A2: {res2}")


if __name__ == '__main__':
    main()