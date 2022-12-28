# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import copy, math
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
from joblib import Parallel, delayed, cpu_count
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))


ssum = lambda x: sum(int(i) for i in x)

def fft(ii, dat):
    _dat = ''
    for i in range(*ii):
        patt = [dat[j:j+i+1] for j in range(0, len(dat), i+1)]
        _dat += str(abs(ssum(''.join(patt[1::4])) - ssum(''.join(patt[3::4]))) % 10)
    return _dat


def main():
    # Read
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = [int(i) for i in ln]

    N = len(data)
    pattern = []
    for i in range(N):
        patt = [0] * (i+1) + [1] * (i+1) + [0] * (i+1) + [-1] * (i+1)
        pattern.append((patt * (N // len(patt) + 1))[1:N+1])

    # Part 1
    if True:
        dat = copy.deepcopy(data)
        for _ in range(100):
            _dat = []
            for i in range(N):
                _dat.append(abs(sum(v*p for v, p in zip(dat, pattern[i]))) % 10)
            dat = _dat
        print(f"A1: {''.join(str(i) for i in dat[:8])}")

    # Part 2
    C = cpu_count()
    dat = ''.join(str(i) for i in data) * 10000
    N = len(dat)
    for k in range(100):
        II = (lambda I = math.ceil(N/C): [(c*I, min((c+1)*I, N)) for c in range(C)])()
        dat = Parallel(-1 if sys.gettrace() is None else 1)(delayed(fft)(ii, 'x' + dat) for ii in II)
        dat = ''.join(dat)
        print(k)
    pos = int(''.join(str(i) for i in data[:7]))
    p2 = dat[pos:pos+8]
    print(f"A2: {''.join(str(i) for i in p2)}")


if __name__ == '__main__':
    main()
