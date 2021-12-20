# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import itertools, collections

def main():

    # Read
    data = {}
    da = []; k = -1
    sc = True
    with open('tdata.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                sc = True
            elif sc:
                if len(da) > 0:
                    data.update({k:da})
                    da = []
                k = int(ln[12:14])
                sc = False
            else:
                da += [tuple(int(i) for i in ln.split(','))]
    data.update({k:da})


    # Part 1
    if True:
        comm_no = 12
        
        data_rel = {}
        for k, bea in data.items():
            rel = {}
            for i in range(len(bea)):
                for j in range(i+1,len(bea)):
                    xyz_ = (bea[i][0]-bea[j][0],bea[i][1]-bea[j][1],bea[i][2]-bea[j][2])
                    rel.update({(i, j): [sum(i**2 for i in xyz_), xyz_]})
            data_rel.update({k: rel})
        
        xyz = {(0,1,2), (2,0,1), (1,2,0), (0,2,1), (1,0,2), (2,1,0)}
        sig = {(1,1,1),(1,1,-1),(1,-1,1),(1,-1,-1),(-1,1,1),(-1,1,-1),(-1,-1,1),(-1,-1,-1)}
        pairs = {}
        for kk in list(itertools.combinations(data_rel.keys(),2)):
            comm = {}
            for br0, rel0 in data_rel[kk[0]].items():
                for br1, rel1 in data_rel[kk[1]].items():
                    if rel0[0] != rel1[0]:
                        continue
                    com = {}
                    for xy in xyz:
                        for si in sig:
                            if rel0[1] == (lambda R = rel1[1], X = xy, S = si: tuple(S[i] * R[i] for i in X))():
                                com.update({(br0, br1): (xy, si)}) 
                        #         break
                        # if len(com) > 0:
                        #     break
                    if len(com) > 1:
                        raise AssertionError()
                    elif len(com) == 1:
                        comm.update(com)
            if len(comm) >= sum(range(comm_no)):
                idx = pd.DataFrame(0, index = pd.Int64Index({j for i in comm.keys() for j in i[0]}, name = f"[{kk[0]}]"), columns = pd.Int64Index({j for i in comm.keys() for j in i[1]}, name = f"[{kk[1]}]"), dtype = int)
                for i in comm:
                    for j in {(0,0),(0,1),(1,0),(1,1)}:
                        idx.loc[i[0][j[0]],i[1][j[1]]] += 1
                mapp = (lambda I = idx, K = np.where(idx >= comm_no - 1): {int(I.index[i]):int(I.columns[j]) for i,j in zip(K[0],K[1])})()
                assert len(mapp) >= 12
                comb = collections.Counter(comm.values())
                trans = next(iter((lambda C = comb, M = max(comb.values()): {k for k, v in C.items() if v == M})()))  # Transformation: order, direction
                pai = next(iter(k for k, v in comm.items() if v == trans))
                pai = (pai[0][0], pai[1][pai[1].index(mapp[pai[0][0]])])
                da = (lambda D = data[kk[1]][pai[1]], T = trans: tuple(D[i] * s for i, s in zip(T[0],T[1])))()
                trans += (tuple(i-j for i, j in zip(data[kk[0]][pai[0]],da)),)  # Transformation: order, direction, position
                pairs.update({kk: trans})
            elif len(comm) > 0:
                print(f"{kk}: {len(comm)}")
        print(pairs)
        print(len(pairs)) # Mora biti eno manj od števila skenerjev.

                            
        print(f"A1: {0}")
          
    
    # Part 2

    print(f"A2: {0}")


if __name__ == '__main__':
    main()