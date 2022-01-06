# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    enemy = (103, 9, 2)

    # Read
    weap = {'Dagger': (8, 4, 0),
            'Shortsword': (10, 5, 0),
            'Warhammer': (25, 6, 0),
            'Longsword': (40, 7, 0),
            'Greataxe': (74, 8, 0)}
    armo = {'Leather': (13, 0, 1),
            'Chainmail': (31, 0, 2),
            'Splintmail': (53, 0, 3),
            'Bandedmail': (75, 0, 4),
            'Platemail': (102, 0, 5),
            None: (0, 0, 0)}
    ring = {'Damage1': (25, 1, 0),
            'Damage2': (50, 2, 0),
            'Damage3': (100, 3, 0),
            'Defense1': (20, 0, 1),
            'Defense2': (40, 0, 2),
            'Defense3': (80, 0, 3),
            None: (0, 0, 0)}

    # Item combinations
    rings = (lambda R = list(ring.keys()): {(R[i], R[j]) for i in range(len(R)) for j in range(i+1,len(R))})() | {(None, None)}
    rings = {k: (ring[k[0]][0]+ring[k[1]][0], ring[k[0]][1]+ring[k[1]][1], ring[k[0]][2]+ring[k[1]][2]) for k in rings}
    comb = {(w,a) + r: (w_[0]+a_[0]+r_[0], w_[1]+a_[1]+r_[1], w_[2]+a_[2]+r_[2], ) for w, w_ in weap.items() for a, a_ in armo.items() for r, r_ in rings.items()}

    def play(player, enemy):
        pl = player[0]
        en = enemy[0]
        while True:
            en -= max(player[1]-enemy[2],1)
            if en <= 0:
                return True
            pl -= max(enemy[1]-player[2],1)
            if pl <= 0:
                return False

    # Part 1
    com = set(comb.values())
    co = {c[-2:] for c in com}
    win = set()
    for c in co:
        win |= {c} if play((100,) + c, enemy) else set()
    win_cost = {i[0] for i in com if i[1:] in win}
    print(f"A1: {min(win_cost)}")


    # Part 2
    lose = co - win
    lose_cost = {i[0] for i in com if i[1:] in lose}
    print(f"A2: {max(lose_cost)}")


if __name__ == '__main__':
    main()
