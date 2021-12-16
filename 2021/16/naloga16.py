# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = ln

    if 0: #Testing
       data = 'D2FE28'
       data = '38006F45291200'
       data = 'EE00D40C823060'
       
       data = '8A004A801A8002F478'
       data = '620080001611562C8802118E34'
       data = 'C0015000016115A2E0802F182340'
       data = 'A0016C880162017C3686B18A3D4780'
       
       data = 'C200B40A82'
       data = '04005AC33890'
       data = '880086C3E88112'
       data = 'CE00C43D881120'
       data = 'D8005AC2A8F0'
       data = 'F600BC2D8F'
       data = '9C005AC2F8F0'
       data = '9C0141080250320F1802104A08'

    b2i = lambda x: int(x,2)
    h2b = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}
    # Part 1
    dat = ''.join([h2b[i] for i in data])
    if True:
        def parse(data, no = 10**6):
            dat = data
            version = []; type_id = []; literal = []
            k = 0
            while len(dat) >= 11 and k < no:
                ver = b2i(dat[:3])
                typ = b2i(dat[3:6])
                if typ == 4: #literal value
                    lit = ''
                    sub = dat[6:]
                    while True:
                        lit += sub[1:5]
                        if sub[0] == '0':
                            sub = sub[5:]
                            break
                        sub = sub[5:]
                    version += [ver]
                    type_id += [typ]
                    literal += [b2i(lit)]
                    dat = sub
                else: #operatoir
                    if dat[6] == '0': #total length in bits
                        leng = b2i(dat[7:22])
                        sub = dat[22:22+leng]
                        ve, ty, li, da = parse(sub)
                        dat = dat[22+leng:]
                    else: #number of pockets
                        leng = b2i(dat[7:18])
                        sub = dat[18:]
                        ve, ty, li, da = parse(sub, leng)
                        dat = da
                    version += [ver, ve]
                    type_id += [typ, ty]
                    literal += [None, li]
                k += 1
            return version, type_id, literal, dat

        def ssum(data):
            dat = [ssum(i) if hasattr(i, '__iter__') else i for i in data]
            return sum(dat)


        ve, ty, li, da = parse(dat, 1)
        print(f"A1: {ssum(ve)}")


    # Part 2
    def calc(typ, lit):
        res = []
        for i, t in enumerate(typ):
            if t == 0:
                res += [sum(calc(typ[i+1], lit[i+1]))]
            elif t == 1:
                res += [mat.prod(calc(typ[i+1], lit[i+1]))]
            elif t == 2:
                res += [min(calc(typ[i+1], lit[i+1]))]
            elif t == 3:
                res += [max(calc(typ[i+1], lit[i+1]))]
            elif t == 4:
                res += [lit[i]]
            elif t == 5:
                sub = calc(typ[i+1], lit[i+1])
                res += [1 if sub[0] > sub[1] else 0]
            elif t == 6:
                sub = calc(typ[i+1], lit[i+1])
                res += [1 if sub[0] < sub[1] else 0]
            elif t == 7:
                sub = calc(typ[i+1], lit[i+1])
                res += [1 if sub[0] == sub[1] else 0]
            if i+1 >= len(typ):
                break
        return res

    res2 = calc(ty, li)[0]
    print(f"A2: {res2}")


if __name__ == '__main__':
    main()
