﻿# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
import os, sys, copy, math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
_img_map = {0: '.', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    # Read
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = {i: int(v) for i, v in enumerate(ln.split(','))}

    def intcode(dat, _input = [], pos = 0, base = 0, no_out = None):
        _output = []
        _consumed = []
        address = lambda p, m: p+base if m == 2 else p
        value = lambda p, m: dat.get(address(dat[p],m), 0) if m in {0,2} else dat.get(p, 0)
        while True:
            ins = str(dat[pos])
            ins = (5-len(ins))*'0' + ins
            mod = [int(i) for i in ins[-3::-1]]
            ins = int(ins[-2:])
            if ins == 99:
                stop = True
                break
            if ins == 1:
                assert mod[2] in {0,2}
                dat[address(dat[pos+3], mod[2])] = value(pos+1, mod[0]) + value(pos+2, mod[1])
                pos += 4
            elif ins == 2:
                assert mod[2] in {0,2}
                dat[address(dat[pos+3], mod[2])] = value(pos+1, mod[0]) * value(pos+2, mod[1])
                pos += 4
            elif ins == 3:
                assert mod[0] in {0,2}
                assert len(_input) > 0
                dat[address(dat[pos+1], mod[0])] = _input[0]
                _consumed += [_input[0]]
                _input = _input[1:]
                pos += 2
            elif ins == 4:
                _output.append(value(pos+1, mod[0]))
                pos += 2
                if no_out is not None and len(_output) >= no_out:
                    stop = False
                    break
            elif ins == 5:
                if value(pos+1, mod[0]) != 0:
                    pos = value(pos+2, mod[1])
                else:
                    pos += 3
            elif ins == 6:
                if value(pos+1, mod[0]) == 0:
                    pos = value(pos+2, mod[1])
                else:
                    pos += 3
            elif ins == 7:
                assert mod[2] in {0,2}
                dat[address(dat[pos+3], mod[2])] = 1 if value(pos+1, mod[0]) < value(pos+2, mod[1]) else 0
                pos += 4
            elif ins == 8:
                assert mod[2] in {0,2}
                dat[address(dat[pos+3], mod[2])] = 1 if value(pos+1, mod[0]) == value(pos+2, mod[1]) else 0
                pos += 4
            elif ins == 9:
                base += value(pos+1, mod[0])
                pos += 2
            else:
                raise AssertionError
        return dat, _output, -1 if stop else pos, base, _consumed

    # Part 1
    if True:
        N = 50
        scan = np.zeros((N,N)).astype(int)
        for i in range(scan.shape[0]):
            for j in range(scan.shape[1]):
                _dat, out, _pos, _bas, _con = intcode(copy.copy(data), [i, j])
                if out[0] == 1:
                    scan[i,j] = 1
        print(f"A1: {scan.sum()}")
        _img_print(scan)

    # Part 2
    NN = 100
    beam = {}  # Ključ je vrstica, vrednost je tuple, kjer prva številka predstavlja stolpec, kjer se začne 1, druga številka pa stolpec, kjer se začne 0
    i = 0
    _j = 0; j_ = -1
    while True:
        j = _j
        while j <= 72*i:
            _dat, out, _pos, _bas, _con = intcode(copy.copy(data), [i, j])
            if out[0] == 1:
                beam.update({i: (j,)})
                _j = j
                break
            j += 1
        j = max(j, j_)
        while i in beam:
            _dat, out, _pos, _bas, _con = intcode(copy.copy(data), [i, j])
            if out[0] == 0:
                beam.update({i: beam[i] + (j,)})
                j_ = j
                break
            j += 1
        if beam.get(i, (72*i,))[0] + NN <= beam.get(i+1-NN, (None, 0))[1]:
            p2 = (i+1-NN, beam.get(i)[0])
            break
        i += 1
    print(f"A2: {10000*p2[0] + p2[1]}")

if __name__ == '__main__':
    main()
