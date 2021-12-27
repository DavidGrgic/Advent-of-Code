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
    code = {'.':0, 'v': 1, '>': 7, 'x':8}
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [code[d] for d in ln]
            data += [da]
    data = np.array(data)

    sea = lambda d: '\n'.join(''.join({v:k for k, v in code.items()}[j] for j in i) for i in d)
    occ = lambda a, b, o: (lambda x = {(g, h) for g, h in zip(o[0], o[1])}: np.array([(i, j) in x for i, j in zip(a, b)]))()
    pnt = lambda x: {(i,j) for i, j in zip(x[0],x[1])}
    
    def mov(est, sth, axis):
        occupied = (np.append(est[0], sth[0]), np.append(est[1], sth[1]))
        mov = np.mod(est[axis] + 1, data.shape[axis]) if axis else np.mod(sth[axis] + 1, data.shape[axis])
        oc = occ(est[1-axis] if axis else mov, mov if axis else sth[1-axis], occupied)
        if axis:
            est = (np.append(est[0][~oc], est[0][oc]), np.append(mov[~oc], est[1][oc]))
        else:
            sth = (np.append(mov[~oc], sth[0][oc]), np.append(sth[1][~oc], sth[1][oc]))
        return est, sth

    def psea(e,s):
        d = np.zeros(data.shape)
        d[e] = 7
        d[s] += 1
        print(sea(d))
        
    # Part 1
    if True:
        est = np.where(data==7)
        sth = np.where(data==1)
        step = 0
        while True:
            est0 = est; sth0 = sth
            step += 1
            est, sth = mov(est, sth, 1)  # East move
            est, sth = mov(est, sth, 0)  ## South move
            #print(f"\n{step}"); psea(est, sth)
            if pnt(est) == pnt(est0) and pnt(sth) == pnt(sth0):
                break
        print(f"A1: {step}")
    
    # Part 2
    print(f"A2: {0}")


if __name__ == '__main__':
    main()