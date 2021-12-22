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
    #data = [4,8]


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
    zmage = [0,0]
    position = {(tuple(data), (0,0)): 1}  # Kljuc je tuple, kjer je prva elemnt tuple s pozicijama prvega in drugega igralca, drugi element je score prvega in drugega igralca. value je stevilo svetov. Zacnemo z zacetno pozicijo igralcev (kljuc) v enem vesolju (value)
    while True:
        for k in range(2): #Vrzemo kocko 3 krat
            pos = (lambda P = position.items(), K = k: [(i[0][::1-2*K], i[1][::1-2*K], v) for i, v in P])()  # Tupleti s pozicijo metalca (prvo mesto), pozicija sotekmovalca (drugo mesto), stevilo vesolij (tretje mesto)
            pos = (lambda P = pos, M = met3.items(): [((p[0][0]+pm, p[0][1]), p[1], p[-1]*v) for p in P for pm, v in M])() # Prvi igralec vrze kocko in se premakne po poziciji naprej, istočasno tudi generira nova vesolja
            pos = (lambda P = pos, T = track: [((i[0][0] % T, i[0][1]),) + i[1:] for i in P])()  # Obrat igralne plosce
            pos = (lambda P = pos, T = track: [i if i[0][0] != 0 else ((T, i[0][1]),) + i[1:] for i in P])()   # Koregiramo pozicijo 0 v 10 na igralni plošči
            pos = [i[:1] + ((i[1][0]+i[0][0], i[1][1]),) + i[2:] for i in pos] # Preštejemo točke, pazi samo trenutnemu igralcu
            position = (lambda P = pos, K = k: {tuple(i[::1-2*K] for i in j[:2]): sum(k[2] for k in P if k[:2] == j) for j in {i[:2] for i in P}})()  # Kompresiramo mesta na igralni plošči in obenem se uredimo vrstni red igralcev
            #print(len(position))
            # Koliko iger je dobilo zmagovalca?
            zma = (lambda P = position.items(), K = k: {i: v for i, v in P if i[1][K] >= 21})()
            if len(zma) > 0:
                position = (lambda P = position.items(), Z = zma: {k: v for k, v in P if k not in Z})()
                zmage[k] = zmage[k] + sum(zma.values())
            if len(position) == 0:
                break
        if len(position) == 0:
            break
            
    print(f"A2: {max(zmage)}")


if __name__ == '__main__':
    main()
