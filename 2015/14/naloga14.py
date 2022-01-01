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
            da0 = ln.split(' can fly ')
            da1 = da0[1].split(' km/s for ')
            da2 = da1[1].split(' seconds, but then must rest for ')
            data.update({da0[0]: (int(da1[0]), int(da2[0]), int(da2[1].split()[0]))})

    def distance(sec):
        dist = {}
        for k, v in data.items():
            perioda = sum(v[1:])
            dist.update({k: v[0] * ( v[1] * int(sec / perioda) + (v[1] if (sec % perioda) >= v[1] else (sec % perioda)))})
        return dist

    # Part 1
    seco = 1000
    seco = 2503
    dist = distance(seco)
    print(f"A1: {max(dist.values())}")


    # Part 2
    score = {k:0 for k in data}
    for sc in range(1, seco+1):
        dist = distance(sc)
        dis = max(dist.values())
        for i in {k for k, v in dist.items() if v == dis}:
            score[i] += 1
    print(f"A2: {max(score.values())}")


if __name__ == '__main__':
    main()