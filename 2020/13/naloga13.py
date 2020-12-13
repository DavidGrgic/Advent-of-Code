# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd

def main():
    
    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            if c == 0:
                ts = int(eval(ln))
            elif c == 1:
                sc = ln.split(',')
    sc = [None if i == 'x' else int(i) for i in sc]

    # Part 1
    d1 = []
    for i in sc:
        if i is not None:
            t = int(ts / i) + 1
            d1 += [t*i - ts]
        else:
            d1 += [None]
    mi = min([i for i in d1 if i is not None])
    i = d1.index(mi)
    bus = sc[i]
    print(mi*bus)

    # Part 2
    b_ = []; i_ = []
    for i, b in enumerate(sc):
        if b is not None:
            b_ += [b]
            i_ += [i]
    o_ = [0] * len(b_)
    while len(b_) > 1:
        bM = max(b_)
        j = b_.index(bM)
        iM = i_[j]
        oM = o_[j]
        b_t = b_[:j] + b_[j+1:]
        i_t = i_[:j] + i_[j+1:]
        o_t = o_[:j] + o_[j+1:]
        bm = max(b_t)
        j = b_t.index(bm)
        im = i_t[j]

        p = 0
        ttt = []
        while True:
            ts = oM + p * bM - iM
            if (ts + im) % bm == 0:
                ttt += [ts]
                if len(ttt) == 2:
                    break
            p += 1

        b_ = b_t[:j] + b_t[j+1:] + [ttt[1] - ttt[0]]
        i_ = i_t[:j] + i_t[j+1:] + [0]
        o_ = o_t[:j] + o_t[j+1:] + [ttt[0]]
    print(ttt[0])
        
        

if __name__ == '__main__':
    main()
