# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import pickle
import mat

def main():
#    hodnik = {0: (None,1,None), 1: (0,2,None), 2: (1,3,20), 3: (2,4, None), 4: (3,5,40, None), 5: (4,6,None), 6: (5,7,60), 7: (6,8,None), 8: (7,9,80), 9: (8,10,None), 10: (9,None,None)}
    povezave = ({0,1}, {1,2}, {2,3}, {3,4}, {4,5}, {5,6}, {6,7}, {7,8}, {8,9}, {9,10}, {2,20}, {20,21}, {4,40}, {40,41}, {6,60}, {60,61}, {8,80}, {80,81})
    prostor = (lambda P = povezave: {k: {j for i in P if k in i for j in i-{k}} for k in {j for i in P for j in i}})()
    # Hodnik so pozicije od 0 do 10, sobe so pozicije 20, 21 (pripeti na hodnik 2), 40, 41 (pripeti na hodnik 4), itd
    amph = {('a',0): 21, ('a',1): 81, ('b',0): 20, ('b',1): 60, ('c',0): 40, ('c',1): 61, ('d',0): 41, ('d',1): 80}  # Test data
    #amph = {('a',0): [41], ('a',1): [81], ('b',0): [21], ('b',1): [61], ('c',0): [60], ('c',1): [80], ('d',0): [20], ('d',1): [40]}  # My data

    def move(sedaj, zasedeni, prej = set()):
        kam = prostor[sedaj] - prej - zasedeni
        for k in kam:
            move(k, zasedeni, sedaj)
        return [[sedaj] + r for r in res]

    # Part 1
    def first(state, moved = set()):
        for amp in {k: v for k, v in state.items() if k not in moved}.items():
            pass
    
    
    first(amph)
    print(f"A1: {0}")
          
    
    # Part 2

    print(f"A2: {0}")


if __name__ == '__main__':
    main()
