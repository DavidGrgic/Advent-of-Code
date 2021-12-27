# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import pickle
import collections
import mat
import cProfile, pstats

def main():
    energy = {a: 10**e for a, e in zip(('a','b','c','d'), range(4))}
    target = {'a':20, 'b':40, 'c':60, 'd':80}

    part = 2  # Part with my data (1, 2) or with test data (3, 4)
    if part in {1,3}:  # Part 1
        povezava = ({0,1}, {1,2}, {2,3}, {3,4}, {4,5}, {5,6}, {6,7}, {7,8}, {8,9}, {9,10}, {2,20}, {20,21}, {4,40}, {40,41}, {6,60}, {60,61}, {8,80}, {80,81})  # Hodnik so pozicije od 0 do 10, sobe so pozicije 20, 21 (pripeti na hodnik 2), 40, 41 (pripeti na hodnik 4), itd
        amph = (('a',0), ('a',1), ('b',0), ('b',1), ('c',0), ('c',1), ('d',0), ('d',1))
        if part >= 3:
            posi = (     21,      81,      20,      60,      40,      61,      41,     80)  # Test data, pozicije
        else:
            posi = (     41,      81,      21,      61,      60,      80,      20,     40)  # My data, pozicije
    elif part in {2,4}:  # Part 2
        povezava = ({0,1}, {1,2}, {2,3}, {3,4}, {4,5}, {5,6}, {6,7}, {7,8}, {8,9}, {9,10}, {2,20}, {20,21}, {21,22}, {22,23}, {4,40}, {40,41}, {41,42}, {42,43}, {6,60}, {60,61}, {61,62}, {62,63}, {8,80}, {80,81}, {81,82}, {82,83})
        amph = (('a',0), ('a',1), ('a',2), ('a',3), ('b',0), ('b',1), ('b',2), ('b',3), ('c',0), ('c',1), ('c',2), ('c',3), ('d',0), ('d',1), ('d',2), ('d',3))
        if part >= 3:
            posi = (     23,      83,      62,      81,      20,      60,      42,      61,      40,      63,      41,      82,      43,     80,      21,      22)
        else:
            posi = (     43,      83,      62,      81,      23,      63,      42,      61,      60,      80,      41,      82,      20,     40,      21,      22)
    else:    # Test data
        povezava = ({0,1}, {1,2}, {2,3}, {3,4}, {4,5}, {5,6}, {6,7}, {2,20}, {20,21}, {4,40}, {40,41}, {6,60}, {60,61})
        amph = (('a',0), ('a',1), ('b',0), ('b',1), ('c',0), ('c',1))
        posi = (     61,      20,      60,      40,     21,      41)


    cilj = {k: range(target[k],target[k]+v) for k, v in collections.Counter(a[0] for a in amph).items()}
    jilc = {i: k for k, v in cilj.items() for i in v}

    def move(sedaj, zasedeni, prej = None):
        kam = prostor[sedaj] - (set() if prej is None else {prej}) - zasedeni   # Kam lahko gremo od kjer smo sedaj?
        if sedaj in krizisce or (sedaj > 10 and prej is not None and sedaj < prej and len(kam) > 0): # Gremo kar naprej, če smo na križišču. Prav tako gremo naprej navzdol v sobi, če nismo če čisto na koncu
            res = ()
        else:
            res = ((),)
        for k in kam:
            res += move(k, zasedeni, sedaj)
        return tuple((sedaj,) + r for r in res)


    def cikel(state, moves, just_moved = None):
        if all(amph[a][0] == jilc.get(s) for a, s in enumerate(state)):
            return {(state, 0) if _debug else (0,)}
        premik = {i for i, m in enumerate(moves) if m > 0} - {just_moved}
        if len(premik) == 0:  # Vsi so se ze izkoristili svoje poteze in nimamo več kaj početi.
            return set()
        zaseden = set(state)
        stanja = set()
        for amp in premik:
            soba_ciljna = (lambda A = {s for i, s in zip(amph, state) if i[0] == amph[amp][0]}, C = cilj[amph[amp][0]]: tuple(i in A for i in C))()  # Stanje ciljne sobe za konkretnega amp, od zgoraj navzdol. True če je na poziciji v sobi pravi amp, false ce je napacen ali prazno mesto
            if state[amp] > 10 and state[amp] in cilj[amph[amp][0]] and all(soba_ciljna[state[amp] % 10:]):  # Ce so vsi pod njim vključno z njim v pravi sobi, potem ostane kjer je
                continue
            else:
                poti = vsepoti[state[amp]]
                poti = {p for p in poti if len(zaseden.intersection(p[1:])) == 0} # Odstranimo poti, ki vključujejo zasedena mesta (razen na prvem mestu, kjer je trenutni amp)
                poti = [p for p in poti if len(p) != 1]  # Odstranimo poti, kjer se ne premakne
                if moves[amp] == 1: # Če je to njegov zadnji korak, se mora premakniti v svojo ciljno sobo
                    poti = (lambda P = poti, C = cilj[amph[amp][0]]: [p for p in P if p[-1] > 10 and p[-1] in C])()
                poti = (lambda P = poti, C = cilj[amph[amp][0]]: [p for p in P if p[-1] <= 10 or len(p) <= 1 or p[-1] in C])()  # Odstranimo poti, ki se koncajo v sobi, ki ni ciljna soba za to vrsto, ampak samo ce to ni zacetna pozicija!
                poti = (lambda P = poti, S = soba_ciljna: [p for p in P if not (len(p) > 1 and p[-1] > 10 and not all(S[p[-1] % 10 + 1:]))])()  # V končno sobo ne sme iti če je noter kakšen napačne vrste
            poti = (lambda P = poti, E = energy[amph[amp][0]]: [(p, E * (len(p)-1)) for p in P])()  # Dodamo porabo energije
            for pot in poti:
                sta = cikel(state[:amp] + (pot[0][-1],) + state[amp+1:], moves[:amp] + (moves[amp]-1,) + moves[amp+1:], amp)
                len(sta) > 0
                stanja |= {((state,) + s[:-1] + (s[-1] + pot[1],) if _debug else (s[-1] + pot[1],)) for s in sta}
        return (lambda S = stanja, M = min(s[-1] for s in stanja) if len(stanja) > 0 else None: {s for s in S if s[-1] == M})()


    prostor = (lambda P = povezava: {k: {j for i in P if k in i for j in i-{k}} for k in {j for i in P for j in i}})()
    krizisce = {k for k, v in prostor.items() if len(v) >= 3}
    vsepoti = (lambda S = set(prostor) - krizisce: {s: set(p for p in move(s, set()) if not (len(p) >= 2 and p[0] > 10 and p[0] < p[1])) for s in S})()   # Vse možne poti iz neke lokacije, vendar brez poti, ki se začnejo v sobi in vodijo navzdol po sobi

    _debug = part not in [1,2,3,4]
    t0 = time.time()
    stanja = cikel(posi, tuple(2 for i in posi))
    print(time.time() - t0)
    if _debug:  # To spead up debuging, calcualte or read from pickle
        pickle.dump((stanja,), open(f"~stanja{part}", 'wb'))  # (stanja,) = pickle.load(open(f"~stanja{part}", 'rb'))
    print(f"A{part}: {min(s[-1] for s in stanja)}" + (f"   [{len(stanja)} combinations]" if _debug else ""))


if __name__ == '__main__':
    if True:
        main()
    else:
        cProfile.run('main()', 'profile.txt')
        prof = pstats.Stats('profile.txt')
        prof.sort_stats('cumulative').print_stats(30)