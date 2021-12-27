# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import pickle

def main():

    var = {'w', 'x', 'y', 'z'}

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                pass
            da = ln.split(' ')
            if len(da) > 2 and da[2] not in var:
                da[2] = int(da[2])
            data += [tuple(da)]


    def au(sect, w, z):
        v = {'w': w, 'x': 0, 'y': 0, 'z': z}
        for i in sect[1:]:
            b = i[2] if isinstance(i[2], int) else v[i[2]]
            if i[0] == 'add':
                v[i[1]] += b
            elif i[0] == 'mul':
                v[i[1]] *= b
            elif i[0] == 'div':
                v[i[1]] = int(v[i[1]] / b)
            elif i[0] == 'mod':
                v[i[1]] %= b
            elif i[0] == 'eql':
                v[i[1]] = int(v[i[1]] == b)
            else:
                raise AssertionError()
        return v['z']


    # Izgleda, da je program med vhodi sestavljen iz sekcij, med katerimi se prenaša samo spremnljivka 'z', razbijemo na sekcije
    sections = []
    for i, ins in enumerate(data):
        if ins[0] == 'inp':
            if i != 0:
                sections += [sub]
            sub = []
        sub += [ins]
    sections += [sub]
    assert all(i[0] == ('inp', 'w') for i in sections)  # Preverimo, da res na vsaki sekciji vpisemo vhod v register w


    z_init = 0
    z_target = 0
    recalc = True
    if recalc:
        if True:
            stanja = [{z_init}]  # Pazi, začetni element je začetno staje 
            t0 = time.time()
            for i, sect in enumerate(sections[:-1]):  # Zadnje ne rabimo dealat
                stanja += [{au(sect, i, z) for i in range(1,10) for z in stanja[-1]}]
                print(f"{i+1}: {len(stanja[-1])} [{round(100*len(stanja[-1])/(9**(i+1)),6)} %] [{round(time.time()-t0,2)} s]")
            pickle.dump((stanja,), open("~stanja", 'wb'))
        else:
            (stanja,) = pickle.load(open("~stanja", 'rb'))
        valid = [{(None, z_target)}]
        t0 = time.time()
        for i, sect in enumerate(sections[::-1]):
            valid = [(lambda V = {v[1] for v in valid[0]}, S = stanja[-(i+1)]: {(i, z) for i in range(1,10) for z in S if au(sect, i, z) in V})()] + valid
            print(f"{len(sections)-i}: {len(valid[0])}  [{round(time.time()-t0,2)} s]")
        pickle.dump((valid,), open("~valid", 'wb'))
    else:
        (valid,) = pickle.load(open("~valid", 'rb'))

    def unpack(fu):
        res = []
        z = z_init
        for i, val in enumerate(valid):
            r = (lambda M = fu(v[0] for v in val), V = val: {v for v in V if v[0] == M})()
            r = next(iter(r))
            res += [r[0]]
            if len(res) >= len(sections):
                break
            z = au(sections[i], *r)
        return sum(k*10**i for i, k in enumerate(res[::-1]))


    # Part 1
    print(f"A1: {unpack(max)}")

    # Part 2
    print(f"A2: {unpack(min)}")


if __name__ == '__main__':
    main()