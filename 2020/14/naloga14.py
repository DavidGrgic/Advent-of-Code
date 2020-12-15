# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd


def komb(flo):
    if len(flo) > 1:
        tmp = komb(flo[1:])
        res = [i + j for i in [0, 2** (flo[0]-1)] for j in tmp]
    else:
        res = [i for i in [0, 2** (flo[0]-1)]]
    return res


def main():
    
    # Part 1
    mem = {}
    mask = 0
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ins, val = ln.split(' = ')
            if ins == 'mask':
                mask = val.replace('\n', '')
            else:
                ad = int(eval(ins.split('[')[-1][:-1]))
                va = int(eval(val))

                vab = str(bin(va))[2:]
                vab = '0' * (36-len(vab)) + vab
                
                vad = '0b' + ''.join([v if m == 'X' else m for v, m in zip(vab, mask)])
                mem.update({ad: int(eval(vad))})

    print(sum([v for k, v in mem.items()]))

    # Part 2
    mem = {}
    mask = 0
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ins, val = ln.split(' = ')
            if ins == 'mask':
                mask = val.replace('\n', '')
            else:
                ad = int(eval(ins.split('[')[-1][:-1]))
                va = int(eval(val))

                add = str(bin(ad))[2:]
                add = '0' * (36-len(add)) + add
                
                flo = [36-i for i, v in enumerate(mask) if v == 'X']
                kom = komb(flo)
                
                ms = eval('0b' + ''.join(['0' if m == 'X' else (v if m == '0' else '1') for v, m in zip(add, mask)]))
                for i in kom:
                    mem.update({ms + i: int(va)})

    print(sum([v for k, v in mem.items()]))


if __name__ == '__main__':
    main()
