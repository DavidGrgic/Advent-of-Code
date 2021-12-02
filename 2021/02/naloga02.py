# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            ins = ln.split(' ')
            data += [(ins[0], int(ins[1]))]

    # Part 1
    pos = [0,0]
    for i in data:
        if i[0] == 'forward':
            pos[0] += i[1]
        elif i[0] == 'down':
            pos[1] += i[1]
        elif i[0] == 'up':
            pos[1] -= i[1]
        else:
            raise ValueError()
    print(f"A1: {mat.prod(pos)}")
            
    # Part 2
    pos = [0,0,0]
    for i in data:
        if i[0] == 'forward':
            chng = i[1] * pos[2]
            pos[0] += i[1]
            pos[1] += chng
        elif i[0] == 'down':
            pos[2] += i[1]
        elif i[0] == 'up':
            pos[2] -= i[1]
        else:
            raise ValueError()
    print(f"A2: {mat.prod(pos[:2])}")

if __name__ == '__main__':
    main()
