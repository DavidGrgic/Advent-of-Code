# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import itertools

def main():
    
    # Read
    data = {}
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            ing, ale = ln.split(' (contains ')
            data.update({c: (set(ing.split(' ')), set(ale[:-1].split(', ')))})
    ing = {i for v in data.values() for i in v[0]}
    ale = {i for v in data.values() for i in v[1]}

    # Part 1
    # Za vsak alergen poišči presek vseh komponent:
    ale_x = {}
    for a in ale:
        x = (lambda D = data.values(), A = a: [v[0] for v in D if A in v[1]])()
        ale_x.update({a: set.intersection(*(lambda D = data.values(), A = a: [v[0] for v in D if A in v[1]])())})
    # Vse komponente, ki se pojavljajo v preseku
    ing_x = set.union(*ale_x.values())
    ing_n = ing - ing_x
    p1 = (lambda D = data.values(), I = ing_n: [i for v in D for i in v[0] if i in I])()
    print(len(p1))


    # Part 2
    dat = (lambda D = data.items(), I = ing_x: {k: (v[0] & I, v[1]) for k, v in D})() # Očiščeni podatki s komponentami, ki ne vsebujeo alergenov

    ale_p = list(itertools.permutations(ale)) # Permutation of all alergens

    ing_p = list(ing_x)
    ii = []
    for i, a in enumerate(ale_p):
        ing_ale = {i: a for i, a in zip(ing_p, a)}
        chk = True
        for k, v in dat.items():
            x = (lambda I = v[0], X = ing_ale: {X.get(i) for i in I})()
            if not all((lambda V = v[1], X = x: [i in X for i in V])()):
                chk = False
                break
        if chk:
            ii += [i]

    if len(ii) != 1:
        raise
    p2 = ','.join(pd.Series(ing_p, index = ale_p[ii[0]]).sort_index().values)
    print(p2)

if __name__ == '__main__':
    main()
