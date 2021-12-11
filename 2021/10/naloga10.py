# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np, time
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data += [ln]


    pairs = {('(', ')'), ('[',']'), ('{','}'), ('<','>')}
    s_e = {i[0]:i[1] for i in pairs}
    wei = {')':3, ']':57, '}': 1197, '>':25137}
    # Part 1
    def chk(da):  # First return is corrupt indicator, incompleate, second is remaining part
        if da[0] not in s_e:
            return True, False, da
        elif len(da) <= 1:
 #           print(da)
            return False, True, da
        else:
            if s_e[da[0]] == da[1]:
#                print(da)
                return False, False, da[2:]
            elif da[1] in s_e.values():

                return True, False, da[1:]
            else:
                cc, ii, dd = chk(da[1:])
#                print(dd)
                if cc:
                    return cc, ii, dd
                else:
                    if ii:
                        return cc, ii, da[:1] + dd
                    else:
#                        return cc, ii, da[:1] + dd
                        return chk(da[:1] + dd)

        
        
    
    cor = []
    inc = []
    com = []
    for i, da in enumerate(data):
        sub = sub0 = da
        while True:
            cc, ii, sub = chk(sub)
            if cc or sub == sub0:
                break
            else:
                sub0 = sub
        if cc:
            cor += [sub]
        else:
            inc += [sub]

    if True:
        res1 = (lambda W = wei, C = cor: [W[i[0]]for i in C])()
        print(f"A1: {sum(res1)}")
          
    
    # Part 2
    inc = [i[::-1] for i in inc]
    inc = [''.join(s_e[j] for j in i) for i in inc]
    wei = {')':1, ']':2, '}':3, '>':4}
    iii = []
    for i in inc:
        v = 0
        for j in i:
            v = 5 * v + wei[j]
        iii += [v]
    iii.sort()
    print(f"A2: {iii[int(len(iii) / 2)]}")


if __name__ == '__main__':
    main()
