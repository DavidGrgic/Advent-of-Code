# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat


def calc(exp):
    
    def okle(okl):
        nivo = 0
        i = 0
        for i, ch in enumerate(okl):
            if ch == '(':
                nivo -= 1
            elif ch == ')':
                nivo += 1
            if nivo == 0:
                break
        s1 = calc(okl[1:i])
        return str(s1) + okl[i+1:]

    while len(exp) > 0:
        ss = exp.split(' ')
        if len(ss) == 1:
            return int(eval(ss[0]))
        if ss[0][0] == '(':
            exp = okle(exp)
            continue
        else:
            if ss[2][0] == '(':
                exp = ' '.join(ss[:2]) + ' ' + okle(' '.join(ss[2:]))
                continue
            s1 = int(eval(ss[0]))
            op = ss[1]
            s2 = int(eval(ss[2]))
            sn = int(eval('{0}{1}{2}'.format(s1, op, s2)))
            exp = ' '.join([str(sn)] + ss[3:])


def advcalc(exp):

    def okle(okl):
        nivo = 0
        i = 0
        for i, ch in enumerate(okl):
            if ch == '(':
                nivo -= 1
            elif ch == ')':
                nivo += 1
            if nivo == 0:
                break
        s1 = advcalc(okl[1:i])
        return str(s1) + okl[i+1:]

    sub = -1
    try:
        sub = exp.index('(')
    except:
        mul = exp.split('*')
        return mat.prod([int(eval(i)) for i in mul])

    if sub >= 0:
        if sub == 0:
            exp = okle(exp)
        else:
            exp = exp[: sub] + okle(exp[sub:])
        return advcalc(exp)


def main():
    
    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            data += [ln.replace('\n', '')]

    # Part 1
    res1 = []
    for i, l in enumerate(data):
        res1 += [calc(l)]
    print(sum(res1))


    # Part 2
    res2 = []
    for i, l in enumerate(data):
        res2 += [advcalc(l)]
    print(sum(res2))

if __name__ == '__main__':
    main()
