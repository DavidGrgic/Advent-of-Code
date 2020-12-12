# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import math

def main():
    
    # Read
    data = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ins = ln[0]
            val = int(eval(ln[1:].replace('\n','')))
            data += [(ins, val)]

    sides = ['N', 'E', 'S', 'W']
    si = {'L': -1, 'R': 1}
    # Part 1
    direction = 'E'
    point = (0,0)
    move = {'N': (0,1), 'E': (1,0), 'S': (0,-1), 'W': (-1,0)}
    for i, v in data:
        if i in {'L', 'R'}:
            t = int(round(v/90))
            direction = sides[(sides.index(direction) + t * si.get(i)) % 4]
        else:
            if i == 'F':
                i = direction
            m = move.get(i)
            point = (point[0] + v * m[0], point[1] + v * m[1])
    print(abs(point[0])+abs(point[1]))


    # Part 2
    wp = (10,1)
    point = (0,0)
    for i, v in data:
        if i in {'L', 'R'}:
            t = int(round(v/90))
            for j in range(t):
                wp1 = wp[0] * (-si.get(i))
                wp0 = wp[1] * (si.get(i))
                wp = (wp0, wp1)
        elif i == 'F':
            point = (point[0] + wp[0]*v, point[1] + wp[1]*v)
        else:
            m = move.get(i)
            wp = (wp[0] + v * m[0], wp[1] + v * m[1])
    print(abs(point[0])+abs(point[1]))
   # print(data)

if __name__ == '__main__':
    main()
