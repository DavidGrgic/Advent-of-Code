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
            da = ln.split(': ')
            data.update({da[0]: tuple(int(i.split()[1]) for i in da[1].split(', '))})


    def generator(length, csum = 0, target = 100):
        if length == 0:
            res = [(target - csum,)]
        else:
            res = []
            for i in range(0, target - csum + 1):
                re = generator(length - 1, csum + i, target)
                res += [(i,) + r for r in re]
        return res
        
    # Part 1
    sestav = data.keys()
    stanja = generator(len(sestav)-1)
    utezi = np.array([data[s][:-1] for s in sestav])
    if True:
        score = {}
        for zlicke in stanja:
            score.update({tuple(zlicke): np.maximum(np.dot(np.array([zlicke]), utezi), 0).prod()})
        print(f"A1: {max(score.values())}")


    # Part 2
    calo = np.array([data[s][-1] for s in sestav])
    score = {}
    for zlicke in stanja:
        if (np.array(zlicke) * calo).sum() == 500:
            score.update({tuple(zlicke): np.maximum(np.dot(np.array([zlicke]), utezi), 0).prod()})
    print(f"A2: {max(score.values())}")


if __name__ == '__main__':
    main()
