# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import time


def chk1(msg, rul, ru = 0, par = []):
    po = sum(len(j) for j in par)
    rr = rul.get(ru)
    if isinstance(rr, str):
        return msg[po] == rr, rr  # Finished this branch, string part
    else:
        for j, o in enumerate(rr):
            pr = ''
            aa = []
            for i, r in enumerate(o):
                ch = chk1(msg, rul, r, par + [pr])
                pr += ch[1]
                aa += [ch[0]]
            if all(aa):
                return True, pr
        return False, ''
        
    
def chk2(msg, rul, ru = 0, par = []):
    po = sum(len(j) for j in par)
    rr = rul.get(ru)
    if isinstance(rr, str):
        if po < len(msg):
            return msg[po] == rr, rr  # Finished this branch, string part
        else:
            return 0, ''
    else:
        for j, o in enumerate(rr):
            if o == (8, 11): # Zanka
                s42 = set(comb(rul, 42))
                s31 = set(comb(rul, 31))
                ln = len(next(iter(s42)))
                tmp = ''
                k42 = 0
                while True:
                    if msg[po + len(tmp): po + len(tmp) + ln] in s42:
                        tmp += msg[po + len(tmp): po + len(tmp) + ln]
                        k42 += 1
                    else:
                        break
                k31 = 0
                while True:
                    if msg[po + len(tmp): po + len(tmp) + ln] in s31:
                        tmp += msg[po + len(tmp): po + len(tmp) + ln]
                        k31 += 1
                    else:
                        break
                if msg[po:] == tmp and 0 < k31 < k42:
                    return True, ''.join(par) + tmp
                else:
                    return False, ''
            else:
                pr = ''
                aa = []
                for i, r in enumerate(o):
                    ch = chk2(msg, rul, r, par + [pr])
                    pr += ch[1]
                    aa += [ch[0]]
                if all(aa):
                    return True, pr
        return False, ''


def comb(rul, ru):
    rr = rul[ru]
    oo = []
    for o in rr:
        aa = ['']
        for a in o:
            ax = comb(rul, a) if isinstance(a, int) else [a]
            aa = [i+j for i in aa for j in ax]
        oo += aa
    return oo


def main():

    # Read
    data = []
    rule = {}
    mode = False
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if len(ln) == 0:
                mode = True
                continue
            if mode:
                data += [ln]
            else:
                ru, val = ln.split(': ')
                va = val.split(' | ')
                w = []
                for v in va:
                    u = []
                    for i in  v.split(' '):
                        try:
                            k = int(i)
                        except:
                            u = i[1]
                            continue
                        u += [k]
                    w += [u if isinstance(u, str) else tuple(u)]
                rule.update({int(ru): w[0] if isinstance(w[0], str) else w})

    x = comb(rule, 0)

    # Part 1
    if True:
        part1 = []
        for msg in data:
            ch = chk1(msg, rule)
            part1 += [ch[0] and ch[1] == msg]
        print(sum(part1))

    # Part 2
    rule.update({8: [(42,), (42, 8)], 11: [(42, 31), (42, 11, 31)]})
       
    part2 = []
    for k, msg in enumerate(data):
        part2 += [chk2(msg, rule)]
    part2 = [i[1] for i in part2 if i[0]]
    print(len(part2))

if __name__ == '__main__':
    main()
