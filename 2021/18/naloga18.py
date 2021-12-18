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
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                pass
            da = eval(ln)
            data += [da]
    data = tuple(data)


    # Part 1
    def red(num):
        
        def fnd_e(nus):
            idx = -1
            glo = 0
            for i, l in enumerate(nus):
                if l == '[':
                    glo += 1
                elif l == ']':
                    glo -= 1
                if glo >= 5:
                    ii = nus[i:].find(']')
                    iii = nus[i:i+ii][::-1].find('[')
                    idx = i + ii - iii - 1
                    break
            return idx

        def fnd_s(nus):
            idx = -1
            for i in range(len(nus)):
                if nus[i:i+2].isnumeric():
                    idx = i
                    break
            return idx

        def sns(ss):
            s1 = ss; nn = ''; s2 = ''
            for k, l in enumerate(ss):
                if l.isnumeric():
                    i = 0
                    while ss[k+i+1].isnumeric():
                        i += 1
                    s1 = ss[:k]
                    nn = ss[k:k+i+1]
                    s2 = ss[k+i+1:]
                    break
            return s1, nn, s2

        def exp1x(nus, idx):
            assert idx >= 0
            left = nus[:idx]
            i = nus[idx:].find(']')
            midd = eval(nus[idx:idx+i+1])
            right = nus[idx+i+1:]
            left = left[::-1]
            s1, nn, s2 = sns(left)
            if nn != '':
                left = s1 + str(int(nn[::-1]) + midd[0])[::-1] + s2
            left = left[::-1]
            s1, nn, s2 = sns(right)
            if nn != '':
                right = s1 + str(int(nn) + midd[1]) + s2
            return left + '0' + right

        def spl1x(nus, idx):
            assert idx >= 0
            nn = int(nus[idx:idx+2])
            nus = nus[:idx] + f"[{int(nn/2)},{int(.5+nn/2)}]" + nus[idx+2:]
            return nus

        nus = str(num).replace(' ', '')
        idx_e = idx_s = 0
        while idx_e >= 0 or idx_s >= 0:
            while idx_e >= 0:
                idx_e = fnd_e(nus)
                if idx_e >= 0:
                    nus = exp1x(nus, idx_e)
            idx_s = fnd_s(nus)
            if idx_s >= 0:
                nus = spl1x(nus, idx_s)
                idx_e = 0
        return eval(nus)

    def mag(num):
        assert len(num) == 2
        for i in range(len(num)):
            if hasattr(num[i], '__iter__'):
                num[i] = mag(num[i])
        return 3 * num[0] + 2 *num[1]


    if True:
        dat = data
        while len(dat) >= 2:
            rac = [dat[0], dat[1]]
            rac = red(rac)
            dat = (rac,) +dat[2:]
        res1 = mag(dat[0])
        print(f"A1: {res1}")
          
    
    # Part 2
    mmag = 0
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            rac1 = red([data[i], data[j]])
            mg = mag(rac1)
            if mg > mmag:
                mmag = mg
            rac2 = red([data[j], data[i]])
            mg = mag(rac2)
            if mg > mmag:
                mmag = mg
    print(f"A2: {mmag}")


if __name__ == '__main__':
    main()