﻿# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    repl = {}
    mo = False
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                mo = True
                continue
            if mo:
                mole = ln
            else:
                da = ln.split(' => ')
                repl.update({da[0]: repl.get(da[0], set()) | {da[1]}})

    def mole_split(mole: str, mol: set):
        res = ()
        while len(mole) > 0:
            fres = {k: v for k, v in {k: mole.find(k) for k in mol}.items() if v >= 0}
            if len(fres) == 0:
                res += (mole,)
                break
            fmin = min(fres.values())
            fres = next(iter(k for k, v in fres.items() if v == fmin))
            res += ((mole[:fmin],) if fmin > 0 else ()) + (fres,)
            mole = mole[fmin + len(fres):]
        return res

    comp = set(repl.keys())
    for i in set(mole_split(mole, comp)) - comp:
        while True:
            tmp = [j.isupper() for j in i]
            tmp = tmp[1:].index(True) if True in tmp[1:] else -1
            if tmp >= 0:
                pass
            else:
                comp |= {i}
                break
    mole = mole_split(mole, comp)
    repl = {k: {mole_split(i, comp) for i in v} for k, v in repl.items()}

    # Part 1
    if True:
        res1 = set()
        for i in range(len(mole)):
            for j in repl.get(mole[i], set()):
                res1 |= {mole[:i] + j + mole[i+1:]}
        print(f"A1: {len(res1)}")
          
    
    # Part 2
    def reduce(mole, globina = 0):
        if mole == ('e',):
            return {(''.join(mole),)} if _debug else {0}
        res = set()
        for i in range(len(mole)):
            for k, v in repl.items():
                for j in v:
                    if j == mole[i: i+len(j)]:
                        re = reduce(mole[:i] + (k,) + mole[i+len(j):], globina + 1)
                        res |= {(''.join(mole),) + r for r in re} if _debug else {1 + r for r in re}
            if globina <= 8: print(globina * "\t" + f"{i}/{len(mole)}")
        return res

    _debug = False
    t0 = time.time()
    res2 = reduce(mole)
    print(time.time()-t0)
    res2 = {len(i)-1 for i in res2} if _debug else res2
    print(f"A2: {min(res2)}")


if __name__ == '__main__':
    main()