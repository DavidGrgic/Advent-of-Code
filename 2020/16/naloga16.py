# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd


def prod(x):
    if hasattr(x, '__iter__'):
        y = x[0]
        if len(x) > 1:
            y *= prod(x[1:])
    else:
        y = x
    return y


def main():
    
    # Read
    polja = {}
    moja = None
    karte = []
    blok = 0
    k = 0
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == 'your ticket:':
                blok = 1
                continue
            elif ln == 'nearby tickets:':
                blok = 2
                continue
            elif len(ln) == 0:
                continue
            if blok == 0:
                valid = set()
                ins, val = ln.split(': ')
                for v in val.split(' or '):
                    v = v.split('-')
                    valid |= set(range(int(eval(v[0])), 1+int(eval(v[1]))))
                polja.update({k: (valid, ins)})
                k += 1
            elif blok == 1:
                moja = tuple(int(eval(i)) for i in ln.split(','))
            elif blok == 2:
                karte += [tuple(int(eval(i)) for i in ln.split(','))]

    # Part 1
    allvalid = set()
    for k, v in polja.items():
        allvalid |= v[0]
    slabe = []
    bkarte = []
    for j, k in enumerate(karte):
        for i, p in enumerate(k):
            if p not in allvalid:
                slabe += [p]
                bkarte += [j]
    print(sum(slabe))

    # Part 2
    nkarte = []
    for i, k in enumerate(karte):
        if i not in bkarte:
            nkarte += [k]
    mapp = {}
    for i, v in polja.items():
        pozicije = set()
        for j in range(len(polja)):
            test = True
            for k in nkarte:
                if k[j] not in v[0]:
                    test = False
                    continue
            if test:
                pozicije |= set((j,))
        mapp.update({i:pozicije})
    m = pd.Series({i: len(v) for i, v in mapp.items()}).sort_values()
    mm = {}
    for i, v in m.iteritems():
        mm.update({int(i): int(next(iter(mapp[i] - set(mm.values()))))})
    po = {v[1]: i for i, v in polja.items() if v[1][:9] == 'departure'}
    #K = [v for k, v in mm.items() if k <= 5]
    K = (lambda P = po.values(), M = mm.items(): [v for k, v in M if k in P])()
    KK = (lambda K = K, moja= moja: [moja[i] for i in K])()
    print(prod(KK))


if __name__ == '__main__':
    main()
