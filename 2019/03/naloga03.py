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
    data = {}
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data.update({len(data): ln.split(',')})

    def path(pot):
        point = [(0,0)]
        smer = {'R':(1,0), 'U':(0,1), 'L':(-1,0), 'D':(0,-1)}
        addp = lambda x, y: (x[0]+y[0], x[1]+y[1])
        for p in pot:
            sm = smer[p[0]]
            for _ in range(int(p[1:])):
                point += [addp(point[-1], sm)]
        return point

    # Part 1
    poti = {}
    for k, v in data.items():
        poti[k] = path(v)
    krizanje = set(poti[0]).intersection(set(poti[1])) - {(0,0)}
    if True:
        dist = [abs(i[0])+abs(i[1]) for i in krizanje]
        print(f"A1: {min(dist)}")
          
    
    # Part 2
    dis = {poti[0].index(i)+poti[1].index(i) for i in krizanje}
    print(f"A2: {min(dis)}")


if __name__ == '__main__':
    main()
