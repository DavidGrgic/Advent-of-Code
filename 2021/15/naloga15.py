# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import networkx

def main():

    # Read
    data0 = []
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = [int(i) for i in ln]
            data0 += [da]
    data0 = np.array(data0).astype(int)


    def sh_pot(data):
        dat = []
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                for xy in {(0,1), (0,-1), (1,0), (-1,0)}:
                    x = i+xy[0]; y = j+xy[1]
                    if x < 0 or x > data.shape[0]-1 or y < 0 or y > data.shape[1]-1:
                        continue
                    dat += [[(i,j), (x,y), data[x, y]]]
        dat = pd.DataFrame(dat, columns = ['S', 'D', 'W'])
        graf = networkx.from_pandas_edgelist(dat, 'S', 'D', 'W', networkx.DiGraph())
        pot = networkx.shortest_path(graf, (0,0), (data.shape[0]-1, data.shape[1]-1), 'W')
        return pot


    # Part 1
    if True:
        data = data0.copy()
        pot = sh_pot(data)
        res1 = (lambda D = data, P = pot: [D[k] for k in P[1:]])()
        print(f"A1: {sum(res1)}")


    # Part 2
    data = []
    for i in range(5):
        dat = []
        for j in range(5):
            dat += [data0 + i + j]
        data += [np.concatenate(dat, axis = 1)]
    data = np.concatenate(data, axis = 0)
    while True:
        K = data > 9
        if not K.any():
            break
        data[K] -= 9
    pot = sh_pot(data)
    res2 = (lambda D = data, P = pot: [D[k] for k in P[1:]])()
    print(f"A2: {sum(res2)}")


if __name__ == '__main__':
    main()
