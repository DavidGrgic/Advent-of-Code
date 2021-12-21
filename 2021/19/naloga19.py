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

        def transformation(beacons, trans):
            """
            trans:
            Prvi tuple je vrstni red kako morajo biti premetani vhodni elemente, da so potem po istem vrstnem redu kot referenca
            Drugi tuple je predznak vhodov, da smeri ustrezajo referenčnem smerem
            Tretju tuple je izhodišče koordinatneg sistema glede na refereco
            """
            res = []
            for bea in beacons:
                pos = (lambda B = bea, T = trans: tuple(s*B[i] for i, s in zip(T[0],T[1])))()
                pos = (lambda P = pos, R = trans[2]: tuple(p+r for p, r in zip(P, R)))()
   #             pos = (lambda B = bea, T = trans: tuple(p+s*B[k] for i, k, s, p in zip(range(len(B)), T[0], T[1], T[2])))()
                res += [pos]
            return res

        def trans_inv():
            pass
        
        def trans_join(trans, trans_ref):
            # Join transformation on reference transformation
            po = (lambda T = trans[0], I = trans_ref[0]: tuple(T[i] for i in I))()
            si = (lambda S = trans[1], S0 = trans_ref[1], I = trans_ref[0]: tuple(S[i]*s for i,s in zip(I,S0)))()
            re = (lambda R = trans[2], R0 = trans_ref[2], S0 = trans_ref[1], I = trans_ref[0]: tuple(s*R[i] + r for i,s,r in zip(I,S0,R0)))()
            return (po, si, re)


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
                    r0 = mat.iter_abs(rel0[1])
                    r1 = mat.iter_abs(rel1[1])
                    for xy in xyz:
                        if r0 == tuple(r1[i] for i in xy):
                            comm[(br0, br1, xy)] = 1 + comm.get((br0, br1, xy), 0)
            if len(comm) >= sum(range(comm_no)):
                order = {k: sum(v for j, v in comm.items() if j[2] == k) for k in {i[2] for i in comm}}
                order = next(iter(k for k, v in order.items() if v == max(order.values())))
                comm = {k[:2]: v for k, v in comm.items() if k[2] == order}
                idx = pd.DataFrame(0, index = pd.Int64Index({j for i in comm.keys() for j in i[0]}, name = f"[{kk[0]}]"), columns = pd.Int64Index({j for i in comm.keys() for j in i[1]}, name = f"[{kk[1]}]"), dtype = int)
                for i in comm:
                    for j in {(0,0),(0,1),(1,0),(1,1)}:
                        idx.loc[i[0][j[0]],i[1][j[1]]] += 1
                mapp = (lambda I = idx, K = np.where(idx >= comm_no - 1): {int(I.index[i]):int(I.columns[j]) for i,j in zip(K[0],K[1])})()
                assert len(mapp) >= comm_no

                pai = (lambda D = data, M = mapp.items(), O = order, K = kk: [(D[K[0]][i], tuple(D[K[1]][j][k] for k in O)) for i, j in M])()
                for si in sig:
                    comb = (lambda P = pai, S = si: {tuple(i - j for i, j in zip(k[0], tuple(v*s for v, s in zip(k[1], S)))) for k in P})()
                    if len(comb) == 1:
                        break
                assert len(comb) == 1 # Vsi pari nimajo iste orientaciej
                pairs.update({kk: (order, si, next(iter(comb)))})
            elif len(comm) > 0:
                print(f"{kk}: {len(comm)}")
        assert len(pairs) >= len(data) - 1
        map0 = {0: ((0,1,2), (1,1,1), (0,0,0))}
        map0.update({i:None for i in data if i not in map0})
        while True:
            not_done = {k for k, v in map0.items() if v is None}
            if len(not_done) == 0:
                break
            to_do = (lambda P = pairs.keys(), N = not_done: [i for i in P if sum([i[0] in N, i[1] in N]) == 1])()
            for pair in to_do:
                if pair[1] in not_done:
                    ref = pair[0]
                    do = pair[1]
                    trans = pairs[(ref, do)]
                elif pair[0] in not_done:
                    ref = pair[1]
                    do = pair[0]
                    trans = pairs[(ref,  do)]
                    trans = trans_inv(trans)
                else:
                    raise RuntimeError()
                if ref == 0:
                    map0[do] = trans
                else:
                    trans = trans_join(trans, map0[ref])
                    map0[do] = trans

        print(f"A1: {0}")
          
    
    # Part 2

    print(f"A2: {0}")


if __name__ == '__main__':
    main()
"""
R-referenčni senzor
S-senzor
B-beacon

........B
.........
.....S...
.R.......

B je na lokaciji (4,1) napram R. prva os je vodoravna (narašča >), druga je navpična (^).
če ima sonzor B osi (0,1) in sign (1,1): B je na lokaciji (3,2) napram S in (7,3) napram R
če ima sonzor B osi (0,1) in sign (1,-1): B je na lokaciji (3,-2) napram S in (7,3) napram R
če ima sonzor B osi (0,1) in sign (-1,1): B je na lokaciji (-3,2) napram S in (7,3) napram R
če ima sonzor B osi (0,1) in sign (-1,-1): B je na lokaciji (-3,-2) napram S in (7,3) napram R
če ima sonzor B osi (1,0) in sign (1,1): B je na lokaciji (2,3) napram S in (7,3) napram R
če ima sonzor B osi (1,0) in sign (1,-1): B je na lokaciji (2,-3) napram S in (7,3) napram R
če ima sonzor B osi (1,0) in sign (-1,1): B je na lokaciji (-2,3) napram S in (7,3) napram R
če ima sonzor B osi (1,0) in sign (-1,-1): B je na lokaciji (-2,-3) napram S in (7,3) napram R
"""