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


class IntCode():
    
    def __init__(self, code: list[int], input_ = None):
        self.pointer = 0
        self.base = 0
        assert isinstance(code, (list, tuple, dict))
        self.code_ = code.copy() if isinstance(code, dict) else {i: int(v) for i, v in enumerate(code)}
        self.input_ = [] if input_ is None else [[int(i) for i in input_]]
        self.input_consumed = []
        self.output_ = []
        
    
    def __repr__(self):
        return f"pointer={self.pointer}: base={self.base}\n{','.join(str(i) for i in self.code())}"
    
    def run(self, input_ = None):
        address = lambda offset: self.code_[self.pointer+offset] + (self.base if mode[offset-1] == 2 else 0)
        value = lambda offset: self.code_.get(self.pointer+offset, 0) if mode[offset-1] == 1 else self.code_.get(address(offset), 0)
        if input_ is not None:
            self.input_add(input_)
        while True:
            instruction = self.code_[self.pointer]
            mode = [int(i) for i in str(instruction // 100).rjust(3,'0')[::-1]]
            match instruction % 100:
                case 99:
                    self.pointer += 1
                    status = None
                    break
                case 1:  # Add by position
                    self.code_[address(3)] = value(1) + value(2)
                    self.pointer += 4
                case 2:  # Multiply by position
                    self.code_[address(3)] = value(1) * value(2)
                    self.pointer += 4
                case 3:
                    if len(self.input_) > 0:
                        in_ = self.input_.pop(0)
                        self.code_[address(1)] = in_
                        self.input_consumed.append(in_)
                        self.pointer += 2
                    else:
                        status = True
                        break
                case 4:
                    self.output_.append(self.code_[address(1)])
                    self.pointer += 2
                case 5:
                    if value(1) != 0:
                        self.pointer = value(2)
                    else:
                        self.pointer += 3
                case 6:
                    if value(1) == 0:
                        self.pointer = value(2)
                    else:
                        self.pointer += 3
                case 7:
                    self.code_[address(3)] = 1 if value(1) < value(2) else 0
                    self.pointer += 4
                case 8:
                    self.code_[address(3)] = 1 if value(1) == value(2) else 0
                    self.pointer += 4
                case 9:
                    self.base += value(1)
                    self.pointer += 2
                case _:
                    raise RuntimeError('Something went wrong.')
        return status  # None: Program terminated, True: Waiting for input

    def input_add(self, input_):
        self.input_.extend([int(i) for i in input_] if hasattr(input_, '__iter__') else [int(input_)])
        
    def output(self):
        return self.output_

    def code(self):
        return list(i[1] for i in sorted(self.code_.items()))

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

def read(filename):
    with open(filename, 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = {i: int(v) for i, v in enumerate(ln.split(','))}
    return data

def day02():
    t0 = IntCode([1,9,10,3,2,3,11,0,99,30,40,50]); t0.run()
    assert t0.code_[0] == 3500
    t1 = IntCode([1,0,0,0,99]); t1.run()
    assert t1.code() == [2,0,0,0,99]
    t2 = IntCode([2,3,0,3,99]); t2.run()
    assert t2.code() == [2,3,0,6,99]
    t3 = IntCode([2,4,4,5,99,0]); t3.run()
    assert t3.code() == [2,4,4,5,99,9801]
    t4 = IntCode([1,1,1,4,99,5,6,0,99]); t4.run()
    assert t4.code() == [30,1,1,4,2,5,6,0,99]
    data = read(r'.\..\02\data.txt')
    dat = data.copy(); dat[1] = 12; dat[2] = 2
    #_dat, out, _pos, _bas, _con = intcode(dat.copy())
    p1 = IntCode(dat); p1.run()
    assert p1.code_[0] == 2842648

def day05():
    t0 = IntCode([3,0,4,0,99]); assert t0.run()
    t0.run(-72)
    assert t0.output() == [-72]
    t1 = IntCode([1002,4,3,4,33]); t1.run()
    assert t1.code() == [1002, 4, 3, 4, 99]
    t2 = IntCode([1101,100,-1,4,0]); t2.run()
    assert t2.code() == [1101, 100, -1, 4, 99]
    data = read(r'.\..\05\data.txt')
    p1 = IntCode(data); p1.run(1)
    assert p1.output()[-1] == 13547311
    t3 = IntCode([3,9,8,9,10,9,4,9,99,-1,8]); t3.run(9)
    assert t3.output() == [0]
    p2 = IntCode(data); p2.run(5)
    assert p2.output()[-1] == 236453

def day09():
    t0 = IntCode([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]); t0.run()
    assert t0.output() == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    t1 = IntCode([1102,34915192,34915192,7,4,7,99,0]); t1.run()
    assert t1.output() == [1219070632396864]
    t2 = IntCode([104,1125899906842624,99]); t2.run()
    assert t2.output() == [1125899906842624]

def main():
    data = read('d.txt')

    # Part 1
    if True:
        vhod = {k: [k, -1] for k in range(50)}
        izhod = {}
        no = {}
        for k, i in vhod.items():
            j = 0
            while True:
                try:
                    _dat, out, _pos, _bas, _con = intcode(copy.copy(data), i, no_out = j)
                    izhod.update({k: out})
                    j += 1
                except:
                    no.update({k: j-1})
                    break
        for i in (lambda x = [j for i in izhod.values() for j in i]: [x[i:i+3] for i in range(0, len(x), 3)])():
            try:
                _dat, out, _pos, _bas, _con = intcode(copy.copy(data), i , no_out = 1)
                print('OK')
            except:
                print('Fail')
        print(f"A1: {0}")

    # Part 2
    print(f"A2: {0}")

if __name__ == '__main__':
    day02()
    day05()
    day09()
    main()
