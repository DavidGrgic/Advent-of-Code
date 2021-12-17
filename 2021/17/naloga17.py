# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    data = [(20,30), (-10,-5)] # 45, 112
    data = [(138,184), (-125,-71)] # 7750, 4120
    data = [(153,199), (-114,-75)] # 6441, 3186


    # Part 1
    if True:
        res = {}
        s_xx = range(1, data[0][1] + 1)
        for s_x0 in s_xx:
            s_y0 = data[1][0]
            nad = False
            while not nad:
                s_x = [i for i in range(s_x0, 2*data[1][0], -1)]
                s_y = [s_y0-i for i in range(len(s_x))]
                x = 0; y = 0
                Y = y
                for t in range(len(s_x)): # move
                    x += max(s_x[t],0)
                    y += s_y[t]
                    Y = max(Y,y)
                    if y < data[1][0]:
                        break
                    else:
                        if x > data[0][1]:
                            nad = True
                            break
                        elif x >= data[0][0] and y <= data[1][1]:
                            res.update({(s_x0,s_y0): Y})
                            break
                if y > data[1][1]:
                    nad = True
                else:
                    s_y0 += 1
        res1 = max(res.values())
        print(f"A1: {res1}")


    # Part 2
    print(f"A2: {len(res)}")


if __name__ == '__main__':
    main()
