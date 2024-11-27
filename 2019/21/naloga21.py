# -*- coding: utf-8 -*-
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
        # Skoči če je katera od naslednjih treh (A, B, C) luknja in D ni luknja.
        # ( !A + !B + !C) * D  =  !( A * B * C) * D
        inst = [
            "NOT J J",
            "AND A J",
            "AND B J",
            "AND C J",
            "NOT J J",
            "AND D J",
            "WALK"]
        inp = [ord(j) for i in inst for j in i+'\n']
        _dat, out, _pos, _bas, _con = intcode(copy.copy(data), inp)
        if out[-1] > 300:
            print(f"A1: {out[-1]}")
        else:
            print(''.join(chr(i) for i in out))

    # Part 2
    # Skoči:
    # - če je naslednja (A) luknja
    # - na zalogo, če je ali B ali C luknja in sta D in H polni.
    # !A + ( !B + !C) * D * H
    inst = [
            "NOT B J",
            "NOT C T",
            "OR T J",
            "AND D J",
            "AND H J",
            "NOT A T",
            "OR T J",
        "RUN"]
    inp = [ord(j) for i in inst for j in i+'\n']
    _dat, out, _pos, _bas, _con = intcode(copy.copy(data), inp)
    if out[-1] > 300:
        print(f"A2: {out[-1]}")
    else:
        print(''.join(chr(i) for i in out))

if __name__ == '__main__':
    main()
