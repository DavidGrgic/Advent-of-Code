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
            da = ln.split(' | ')
            data += [[i.split() for i in da]]

    dig = {0:6, 1:2, 2:5, 3:5, 4:4, 5:5, 6:6, 7:3, 8:7, 9:6}
    
    uni = {k: v[0] for k, v in {k: [i for i, v in dig.items() if v == k] for k in set(dig.values())}.items() if len(v) == 1}
    # Part 1
    if True:
        dat = np.array([[len(j) for j in i[1]] for i in data]).astype(int)
        res = np.isin(dat, np.array([i for i in uni.keys()])).sum()
        print(f"A1: {res}")
          
    
    # Part 2
    def dig2num(elementni, enakih, kot):
        da = [[j for j in i] for i in dat[0] if len(i) == elementni]
        dd = (lambda X = [i for i in dat[0][num.index(kot)]], D = da, np = np: [np.isin(d, X).sum() for d in D])()
        return ''.join(da[np.where(np.array(dd) == enakih)[0][0]])

    def preostal(elementni):
        return next(iter({d for d, n in zip(dat[0],num) if len(d) == elementni and n is None}))

    res = []
    for dat in data:
        num = [None for i in range(10)]
        le = [len(j) for j in dat[0]]
        for k, v in uni.items():
            num[le.index(k)] = v
        for k, a in {3: (5, 2, 1), 2: (5, 2, 4), 6: (6, 1, 1), 9: (6, 4, 4)}.items():  # 3 je tisti 5 elementni ki ima natanko dva element enak kot 1; 2 je tisti 5 elementni ki ima natanko dva element enak kot 4; 6 je tisti 6 elementni ki ima natanko en element enak kot 1; 9 je tisti 6 elementni ki ima natanko stiri element enak kot 4
            num[dat[0].index(dig2num(*a))] = k
        for k, a in {5: 5, 0: 6}.items():  # 5 je preostali z 5 elementni; 0 je preostali z 6 elementni; 
            num[dat[0].index(preostal(a))] = k
        dig = (lambda D0 = [{i for i in d} for d in dat[0]], D1 = [{i for i in d} for d in dat[1]], N = num: [N[D0.index(d)] for d in D1 ])()
        res += [int(''.join(str(i) for i in dig))]
    print(f"A2: {sum(res)}")


if __name__ == '__main__':
    main()
