# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import random

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

    def mole_split(mole: str):
        res = ()
        while True:
            tmp = [j.isupper() or j == 'e' for j in mole]
            tmp = tmp[1:].index(True) if True in tmp[1:] else -1
            if tmp >= 0:
                res += (mole[:1+tmp],)
                mole = mole[1+tmp:]
            else:
                res += (mole,)
                break
        return res

    mole = mole_split(mole)
    repl = {k: {mole_split(i) for i in v} for k, v in repl.items()}

    # Part 1
    if True:
        res1 = set()
        for i in range(len(mole)):
            for j in repl.get(mole[i], set()):
                res1 |= {mole[:i] + j + mole[i+1:]}
        print(f"A1: {len(res1)}")
          
    
    # Part 2
    def reduce(mole):
        if mole == ('e',):
            return {(''.join(mole),)}
        res = set()
        for i in range(len(mole)):
            for k, v in repl.items():
                for j in v:
                    if j == mole[i: i+len(j)]:
                        re = reduce(mole[:i] + (k,) + mole[i+len(j):])
                        res |= {(''.join(mole),) + r for r in re}
        return res

    def lucky_reduce():
        """
        Najprej provamo reducirati z najdaljšimi proti najkrajšim nizom, znotraj iste dolžine nize uporabimo naključni vrstnoi red
        """
        rep = {(k, i) for k, v in repl.items() for i in v}
        rep = (lambda R = rep, N = {len(i[1]) for i in rep}: {n: [i for i in R if len(i[1]) == n] for n in N})()
        mol = mole
        res = ()
        while mol != ('e',):
            mol0 = mol
            res += (''.join(mol),)
            for n in sorted(rep, reverse = True):
                match = []
                for re in rep[n]:
                    for i in range(len(mol)-n+1):
                        if re[1] == mol[i:i+n]:
                            match += [(i,) + re]
                if len(match) > 0:
                    ire = match[random.randrange(len(match))]  # Random selection of one match
                    mol = mol[:ire[0]] + (ire[1],) + mol[ire[0]+n:]
                    break
            if mol == mol0:
                mol = mole
                res = []
        return res + (''.join(mol),)

    res2 = lucky_reduce()
    print(f"B2: {len(res2)-1}")
    if len(mole) < 20:
        res2 = reduce(mole)
        res2 = {len(i)-1 for i in res2}
        print(f"A2: {min(res2)}")


if __name__ == '__main__':
    main()
