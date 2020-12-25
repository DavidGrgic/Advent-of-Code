# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import copy
import time
import pickle
        


def main():

    def rotate(l, n):
        return l[n:] + l[:n]


    def calc1(data, nn):


        def pik(li, po, n):
            pi = li[po: po+n] + li[:max(0, po + n - len(li))]
            li = [i for i in li if i not in pi]
            return li, pi
    
        def plac(li, de, pi, cu, cu_v):
            i = li.index(de)
            li = li[:i+1] + pi + li[i+1:]
            li = rotate(li, li.index(cu_v) - cu)
            return li

        prt = lambda: ','.join(str(i) for i in dat[:cu])+',('+str(dat[cu])+'),'+','.join(str(i) for i in dat[cu+1:])

        t0 = time.time()

        dat = copy.copy(data)
        cu = 0
        for k in range(nn):
            if (k % 10) == 0:
                pass
                #print(k+1, round(time.time()-t0, 1))
                #print(k+1, prt())
            
            cu_v = de = dat[cu]
            dat, pick = pik(dat, cu+1, 3)
    
            while True:
                de -= 1
                if de in dat:
                    break
                if de < min(dat):
                    de = max(dat)
                    break
    
            dat = plac(dat, de, pick, cu, cu_v)
    
            cu = (cu + 1) % len(dat)
        return dat


    def calc2(data, moves, nn):
        
        def prt():
            x = [cur]
            for i in range(min(30, len(dat)-1)):
                x += [dat[x[-1]]]
            return '({0}),{1}'.format(x[0], ','.join(str(i) for i in x[1:])) 
    
        t0 = time.time()
        n = 3

        dat = {}
        for i in range(len(data)):
            dat.update({data[i]: data[i+1] if i+1 < len(data) else len(data)+1})
        if nn > len(dat):
            dat.update({**{i:i+1 for i in range(len(dat)+1, nn+1)}, **{nn: data[0]}})
        else:
            dat.update({data[-1]: data[0]})

        cur = data[0]
        for k in range(moves):
            if (k % 10**6) == 0:
                pass
                #print(round(10 * (k+1) / nn, 2), round(time.time()-t0,1))
                #print(k+1, prt())
            
            pik = []
            for i in range(n):
                pik += [dat[cur if i == 0 else pik[i-1]]]

            des = cur
            while True:
                des -= 1
                if des not in pik:
                    break
            if des < 1:
                des = nn
                while des in pik:
                    des -= 1

            dat.update({cur: dat[pik[-1]], des: pik[0], pik[-1]: dat[des]})
            cur = dat[cur]
        return dat


    # Read
    tdata = [3,8,9,1,2,5,4,6,7] # Test
    data = [8,7,2,4,9,5,1,3,6] # Input


    # Part 1
    pp = calc1(data, 10**2)    
    p1 = ''.join(str(i) for i in rotate(pp, pp.index(1))[1:])       
    print(p1)


    # Part 2
    if False: # Test
        NN = 20
        pt = calc1(tdata + list(range(max(data)+1, NN + 1)), 30)
        print(pt)
        pt = calc2n(tdata, 30, NN)
    pp = calc2(data, 10**7, 10**6)
    i2 = pp[1]
    p2 = i2 * pp[i2]
    print(p2)


if __name__ == '__main__':
    main()
