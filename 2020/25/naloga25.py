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
    data = [11239946, 10464955]
    tdata = [5764801, 17807724]


    def kro(sub, lop, dev = 20201227):
        val = 1
        for i in range(lop):
            val *= sub
            val %= dev
        return val

    def krogi(pkey, sub = 7, dev = 20201227):
        val = 1
        k = 0
        while True:
            k += 1
            val *= sub
            val %= dev
            if val == pkey:
                return k
            if k > 10**8:
                raise
        

    # Part 1
    dat = data
    lop = []
    for k in dat:
        x = krogi(k)
        lop += [x]
    ekey = []
    ekey = kro(dat[0], lop[1])
    print(ekey)


if __name__ == '__main__':
    main()
