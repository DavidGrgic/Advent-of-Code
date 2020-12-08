# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd

def main():
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ins, val = ln.split(' ')
            data += [(ins, eval(val))]

    poss = set()
    accu = 0
    pos = 0
    while True:
        if pos in poss:
            break
        poss = poss | {pos}
        i = data[pos]
        if i[0] == 'nop':
            pos += 1
        if i[0] == 'jmp':
            pos += i[1]
        if i[0] == 'acc':
            accu += i[1]
            pos += 1
    print(accu)


    corr = set()
    while True:
        poskusi = True
        
        poss = set()
        accu = 0
        pos = 0
        while True:
            if pos in poss:
                break
            if pos >= len(data):
                break
            poss = poss | {pos}
            i = data[pos]
            
            if pos not in corr and i[0] in {'jmp', 'nop'} and poskusi:
                i = ({'nop': 'jmp', 'jmp': 'nop'}.get(i[0], i[0]), i[1])
                corr = corr | {pos}
                poskusi = False
            
            if i[0] == 'nop':
                pos += 1
            if i[0] == 'jmp':
                pos += i[1]
            if i[0] == 'acc':
                accu += i[1]
                pos += 1
        if pos == len(data):
            break
    print(accu)

if __name__ == '__main__':
    main()
