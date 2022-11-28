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
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = [int(i) for i in ln.split(',')]

    def intcode(dat, _input = [], pos = 0, base = 0, no_out = None):
        _output = []
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
        return dat, _output, -1 if stop else pos, base

    def paint(res = {}):
        xyd = (0,0,'u')
        dat = {i:v for i, v in enumerate(data)}
        pos = bas = 0
        while True:
            dat, out, pos, bas = intcode(dat, [res.get(xyd[:2], 0)], pos, bas, 2)
            if pos < 0 or len(out) < 2:
                break
            res.update({xyd[:2]: out[0]})  # Paint
            xyd = xyd[:2] + (turn[(xyd[2], out[1])],)  # Turn
            mo = move[xyd[2]]
            xyd = (xyd[0]+mo[0], xyd[1]+mo[1], xyd[2]) # Move
        return res

    # Part 1
    turn = {('u',0): 'l', ('u',1): 'r', ('l',0): 'd', ('l',1): 'u', ('d',0): 'r', ('d',1): 'l', ('r',0): 'u', ('r',1): 'd'}
    move = {'u': (-1,0), 'l': (0,-1), 'd': (1,0), 'r': (0,1)}
    if True:
        p1 = paint()
        print(f"A1: {len(p1)}")
          
    
    # Part 2
    p2 = paint({(0,0):1})
    _x = min(i[0] for i in p2)
    x_ = max(i[0] for i in p2)
    _y = min(i[1] for i in p2)
    y_ = max(i[1] for i in p2)
    p2_ = np.zeros((x_ - _x + 1, y_ - _y + 1))
    for k, v in p2.items():
        p2_[k] = v
    _img_print(p2_)


if __name__ == '__main__':
    main()
