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
    data = 'abcdefgh'
    data = 'ghijklmn'
    data = 'hepxcrrq'

    diff = ord('z') - ord('a')

    def chkpass(pas):
        for i in {'i', 'o', 'l'}:
            if i in pas:
                return False
        dif = [ord(pas[i+1]) - ord(pas[i]) for i in range(len(pas)-1)]
        ok = False
        n = 0
        for k in dif:
            if k == 1:
                n += 1
                if n >= 2:
                    ok = True
                    break
            else:
                n = 0
        if not ok:
            return False
        pair = set()
        for i, k in enumerate(dif):
            if k == 0:
                pair |= {pas[i]}
        return len(pair) >= 2

    def nextpass(pas):
        while True:
            for i in range(len(pas)-1,-1,-1):
                re = ord(pas[i]) + 1 - ord('a')
                if re > diff:
                    re =  0
                    over = True
                else:
                    over = False
                pas = pas[:i] + chr(ord('a') + re) + pas[i+1:]
                if not over:
                    break
            if chkpass(pas):
                break
        return pas

    # Part 1
    if True:
        res1 = nextpass(data)
        print(f"A1: {res1}")
          
    
    # Part 2
    res2 = nextpass(res1)
    print(f"A2: {res2}")


if __name__ == '__main__':
    main()