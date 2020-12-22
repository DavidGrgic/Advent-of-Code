# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import copy

def main():

    l2t = lambda d: tuple(tuple(i) for i in d)
    
    def game(data):
        dat0 = copy.copy(data)
        dat = copy.copy(dat0)
        runde =set()
        while all(len(i) != 0 for i in dat):
            
            if l2t(dat) in runde: # Prevent infinitive game!
                #dat = [[dat0[0][0], dat0[1][0]] + dat0[0][1:], dat0[1][1:]]
                return dat0
            else:
                runde |= {l2t(dat)}

            w = None
            x = [dat[0][0], dat[1][0]]
            for k in range(len(dat)):
                dat[k] = dat[k][1:]
            
            if len(dat[0]) >= x[0] and len(dat[1]) >= x[1]: # Go into Recursive
                da = game([dat[0][:x[0]], dat[1][:x[1]]])
                if len(da[0]) > 0:
                    w = 0
                else:
                    w = 1
            else:
                if x[0] > x[1]:
                    w = 0
                elif x[0] < x[1]:
                    w = 1
                else:
                    raise

            if w == 0:
                dat[0] += x
            elif w == 1:
                dat[1] += x[::-1]
            else:
                raise

        return dat


    # Read
    data = []
    k = -1
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if len(ln) == 0:
                continue
            elif ln[:7] == 'Player ':
                data += [[]]
                k += 1
            else:
                data[k] = data[k] + [int(ln)]


    # Part 1
    if True:
        dat = copy.copy(data)
        while all(len(i) != 0 for i in dat):
            x = [dat[0][0], dat[1][0]]
            for k in range(len(dat)):
                dat[k] = dat[k][1:]
            if x[0] > x[1]:
                dat[0] += x
            elif x[0] < x[1]:
                dat[1] += x[::-1]
            else:
                raise
        p1 = [sum([(i+1) * v for i, v in enumerate(k[::-1])]) for k in dat]
        print(p1)


    # Part 2
    dat = game(data)
    p2 = [sum([(i+1) * v for i, v in enumerate(k[::-1])]) for k in dat]
    print(p2)

if __name__ == '__main__':
    main()
