# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
_img_map = {0: ' ', 1: '#', 2: 'x', 3: '_', 4: 'o'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                pass
            da = ln.split(',')
            data += [int(i) for i in da]

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


    def board(out):
        sco = None
        if out[-3] == -1:
            sco = out[-1]
            out = out[:-3]
        bor = np.zeros((max(out[1::3])+1,max(out[0::3])+1)).astype(int)
        for y,x,t in zip(out[1::3], out[0::3], out[2::3]):
            bor[y,x] = int(t)
        bal = np.where(bor == 4)
        pad = np.where(bor == 3)
        return bor, (bal[0][0], bal[1][0]), (pad[0][0], pad[1][0]) if len(pad[0]) > 0 else None, sco


    # Part 1
    if True:
        dat = {i:v for i, v in enumerate(data)}
        _dat, out, _pos, _bas, _con = intcode(dat.copy())
        bor, bal, pad, sco = board(out)
        print(f"A1: {(bor==2).sum()}")

    def play(inp0):
        _dat, out, _pos, _bas, _inp = intcode(dat.copy(), inp0 + [0]*10000)
        bor, bal, pad, sco = board(out)
        num = (bor==2).sum()
        if num == 0:
            return _inp, True
        if len(_inp) <= len(inp0):
            return inp0, False
        if pad is None:
            return inp0, False
        print('\n'); _img_print(bor[:-1,:])
        dis = bal[1] - pad[1]
        sig = np.sign(dis)
        dis = abs(dis)
        for i in {}.get(num, [0,-1,1,-2,2,-3,3]):
            print(num, len(_inp), i)
            ii = dis + i
            col = pad[1]+ii*sig
            if ii <= 0:
                continue
            if col < 0 or col >= bor.shape[1] or bor[pad[0], col] in {1,2}:
                continue
            inp = _inp[:-1].copy()  # Last two moves are already too late, e.g ball can not be recovered from here
            if ii > len(inp) - len(inp0):
                continue
            inp[-ii:] = [sig] * ii
            inp, stat = play(inp)
            if stat:
                return inp, stat
        return inp0, False

    # Part 2
    dat[0] = 2
    inp, stat = play([])
    print(f"A2: {inp}")


if __name__ == '__main__':
    main()
