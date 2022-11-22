# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
from collections import Counter
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
            data = [int(i) for i in ln.split(',')]

    def intcode(dat, _input):
        _output = []
        val = lambda p, m: dat[dat[p]] if m == 0 else dat[p]
        pos = 0
        while True:
            ins = str(dat[pos])
            ins = (5-len(ins))*'0' + ins
            par = [int(i) for i in ins[-3::-1]]
            ins = int(ins[-2:])
            if ins == 99:
                break
            if ins == 1:
                assert par[2] == 0
                dat[dat[pos+3]] = val(pos+1, par[0]) + val(pos+2, par[1])
                pos += 4
            elif ins == 2:
                assert par[2] == 0
                dat[dat[pos+3]] = val(pos+1, par[0]) * val(pos+2, par[1])
                pos += 4
            elif ins == 3:
                assert par[0] == 0
                dat[dat[pos+1]] = _input
                pos += 2
            elif ins == 4:
                _output.append(val(pos+1, par[0]))
                pos += 2
            elif ins == 5:
                if val(pos+1, par[0]) != 0:
                    pos = val(pos+2, par[1])
                else:
                    pos += 3
            elif ins == 6:
                if val(pos+1, par[0]) == 0:
                    pos = val(pos+2, par[1])
                else:
                    pos += 3
            elif ins == 7:
                assert par[2] == 0
                dat[dat[pos+3]] = 1 if val(pos+1, par[0]) < val(pos+2, par[1]) else 0
                pos += 4
            elif ins == 8:
                assert par[2] == 0
                dat[dat[pos+3]] = 1 if val(pos+1, par[0]) == val(pos+2, par[1]) else 0
                pos += 4
            else:
                raise AssertionError
        return dat, _output

    intcode([3,0,4,0,99], -72)
    intcode([1002,4,3,4,33], -72)
    intcode([1101,100,-1,4,0], -72)

    # Part 1
    if True:
        ddd, _out = intcode(data.copy(), 1)
        print(f"A1: {_out[-1]}")
          
    intcode([3,9,8,9,10,9,4,9,99,-1,8], 8)
    intcode([3,9,7,9,10,9,4,9,99,-1,8], 8)
    intcode([3,3,1108,-1,8,3,4,3,99], 8)
    intcode([3,3,1107,-1,8,3,4,3,99], 8)
    intcode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 1)
    intcode([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 1)
    intcode([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 8)
    # Part 2
    ddd, _out = intcode(data.copy(), 5)
    print(f"A2: {_out[-1]}")


if __name__ == '__main__':
    main()
