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
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    # Read
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = {i: int(v) for i, v in enumerate(ln.split(','))}

    smer = {'<': (0,-1), 'v': (1,0), '>': (0,1), '^': (-1,0)}
    plus = lambda x, y: (x[0]+y[0], x[1]+y[1])
    sukaj = lambda s, d, S = list(smer.values()): S[(S.index(s) + (1 if d == 'L' else -1)) % len(S)]

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
        dat = copy.deepcopy(data)
        _dat, out, _pos, _bas, _con = intcode(dat)
        #print(''.join(chr(i) for i in out))
        cam = {}
        i = j = 0
        for v in out:
            if v == 10:
                i += 1
                j = 0
                continue
            cam.update({(i,j): v})
            j += 1
        inter = set()
        for k in {k for k, v in cam.items() if v == 35}:
            if sum(cam.get(plus(k, i)) == 35 for i in {(1,0), (-1,0), (0,1), (0,-1)}) == 4:
                inter |= {k}
        p1 = sum(math.prod(i) for i in inter)
        print(f"A1: {p1}")

    # Part 2
    dat = copy.deepcopy(data)
    dat[0] = 2
    pos = next(iter({k for k, v in cam.items() if v in {ord(i) for i in smer}}))
    smr = smer[chr(cam[pos])]
    instr = []
    while True:
        _pos = plus(pos, smr)
        if cam.get(_pos) == 35:
            pos = _pos
            if len(instr) == 0 or not isinstance(instr[-1], int):
                instr.append(0)
            instr[-1] += 1
            continue
        obrat = False
        for i in {'L', 'R'}:
            _smr = sukaj(smr, i)
            if cam.get(plus(pos, _smr)) == 35:
                smr = _smr
                instr.append(i)
                obrat = True
                break
        if not obrat:
            break
    instr = [str(i) for i in instr]
    fun  = []
    _instr = [copy.deepcopy(instr)]
    while len(_instr) > 0:
        cumlen = [len(','.join(_instr[0][:i+1])) for i in range(len(_instr[0]))]
        subfun = [_instr[0][i] for i, v in enumerate(cumlen) if v <= 20]
        subfun = subfun[: 2* (len(subfun) // 2)]
        p = 0
        while True:
            if len(','.join(subfun)) <= 20:
                break
            _p = ','.join(_instr[0]).find(','.join(subfun), p+1)
            if p == 0 and _p == -1:
                subfun = subfun[:-1]
                continue
            elif p == 0 and _p > 0:
                break
        fun.append(','.join(subfun))
        _instr = [j.split(',') for i in _instr for j in ','.join(i).split(fun[-1])]
        _instr = [[j for j in i if j != ''] for i in _instr]
        _instr = [i for i in _instr if len(i) > 0]
    assert len(fun) <= 3
    fun = {chr(ord('A') + i): v for i, v in enumerate(fun)}
    rut = ','.join(instr)
    for k, v in fun.items():
        rut = rut.replace(v, k)
    assert len(rut) <= 20
    _in =  [ord(i) for i in '\n'.join([rut] + list(fun.values()) + ['n\n'])]
    _dat, out, _pos, _bas, _con = intcode(dat, _in)
    print(f"A2: {out[-1]}")


if __name__ == '__main__':
    main()
