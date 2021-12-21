# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import collections

def main():

    # Read
    data = [10,1]
    data = [4,8]


    # Part 1
    if True:
        pos = data.copy()
        
        score = [0,0]
        track = 10
        die_m = 100
        die = 1
        global roll
        roll = 0
        
        def dice(die):
            global roll
            met = []
            for i in range(3):
                roll += 1
                met += [die]
                die += 1
                if die > 100:
                    die = 1
            return sum(met), die
        
        while max(score) < 1000:
            for k in range(2):
                mov, die = dice(die)
                pos[k] = (pos[k] + mov) % track
                if pos[k] == 0:
                    pos[k] = track
                score[k] += pos[k]
                if max(score) >= 1000:
                    break
        print(f"A1: {roll * min(score)}")
          
    
    # Part 2
    die_m = 3
    def met_n(n):
        if n == 0:
            return [()]
        else:
            return [j+(i,) for j in met_n(n-1) for i in range(1,die_m+1)]

    met3 = collections.Counter([sum(i) for i in met_n(3)])
    
    print(f"A2: {0}")


if __name__ == '__main__':
    main()
