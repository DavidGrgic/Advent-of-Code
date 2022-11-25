# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
from collections import Counter
from itertools import permutations, combinations
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += [int(i) for i in ln.split(',')]

    def intcode(dat, _input, pos = 0):
        _output = None
        val = lambda p, m: dat[dat[p]] if m == 0 else dat[p]
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
                assert len(_input) > 0
                dat[dat[pos+1]] = _input[0]
                _input = _input[1:]
                pos += 2
            elif ins == 4:
                _output = val(pos+1, par[0])
                pos += 2
                return dat, pos, _output
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
        return dat, -1, _output

    # Part 1
    if False:
        p1 = {}
        for per in permutations(range(5)):
            val = 0
            for p in per:
                val = intcode(data.copy(), [p, val])[-1][-1]
            p1.update({per: val})
        print(f"A1: {max(p1.values())}")
          
    
    # Part 2
    p2 = {}
    for per in permutations(range(5,10)):
        dat = [data.copy(),data.copy(),data.copy(),data.copy(),data.copy()]; pos = [0] * 5
        val = va = 0
        first = True; halt = False
        while all(i >= 0 for i in pos):
            for i, p in enumerate(per):
                dt, ps, va = intcode(dat[i], [p, va] if first else [va], pos[i])
                dat[i] = dt
                pos[i] = ps
                if ps < 0:
                    halt = True
                    break
            if halt:
                break
            elif i == 4:
                val = va
            first = False
        p2.update({per: val})
    print(f"A2: {max(p2.values())}")


if __name__ == '__main__':
    main()
