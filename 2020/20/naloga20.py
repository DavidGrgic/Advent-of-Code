# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat
import pickle

def main():

    def fnd():
        return {k: xy + (rot, flp)}
    
    def flip(a2d, k = 0):
        if k == 0:
            return a2d
        elif k == 1:
            return pd.np.flip(a2d, axis = 0)
        elif k == 2:
            return pd.np.flip(a2d, axis = 1)
        elif k == 3:
            return pd.np.flip(pd.np.flip(a2d, axis = 0), axis = 1)
        else:
            raise ValueError('Flip paramenter should be 0-3')
    
    def tile_loc(kor, x, y):
        return [k for k, v in kor.items() if v[0] == x and v[1] == y]
        
        
    # Read
    data = {}
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln[:5] == 'Tile ':
                k = int(ln[5:-1])
                dat = []
            elif len(ln) > 1:
                dat += [tuple(1 if i == '#' else 0 for i in ln)]
            else:
                data.update({k: pd.np.array(dat, dtype = int)})
        data.update({k: pd.np.array(dat)})

    # Part 1
    if True:
        kor = {next(iter(data)): (0,0,0,0)} #x, y, rot, flip
        while len(set(data.keys()) - set(kor.keys())) > 0:
            nepregledani = {k for k in data if k not in kor}
            found = None
            for kk, xyrf in kor.items():  # Že locirani
                MM = data[kk].copy()
                MM = pd.np.rot90(MM, xyrf[2])
                MM = flip(MM, xyrf[3])
                for ij in {(1,0), (0,1), (-1,0), (0,-1)}: # Sosednja mesta od lociranega
                    xy = (xyrf[0]+ij[0], xyrf[1]+ij[1])
                    if xy not in {i[:2] for i in kor.values()}:  # samo če je sosednje mesto že prosto
                        for k in nepregledani:   # Primerjamo preostale
                            for rot in range(4):
                                for flp in range(4):
                                    mm = data[k].copy()
                                    mm = pd.np.rot90(mm, rot)
                                    mm = flip(mm, flp)
                                    if ij == (1,0) and (MM[:,-1] == mm [:,0]).all():
                                        found = fnd()
                                    elif ij == (0,1) and (MM[0,:] == mm [-1,:]).all():
                                        found = fnd()
                                    elif ij == (-1,0) and (MM[:,0] == mm [:,-1]).all():
                                        found = fnd()
                                    elif ij == (0,-1) and (MM[-1,:] == mm [0,:]).all():
                                        found = fnd()
                                    if found is not None:
                                        break        
                                if found is not None:
                                    break
                            if found is not None:
                                break
                        if found is not None:
                            break
                if found is not None:
                    break
            if found is not None:
                kor.update(found)
            #print(len(kor))
        pickle.dump((data, kor), open('n20', 'wb'))
    else:
        (data, kor) = pickle.load(open('n20', 'rb'))
    xX = min(v[0] for k, v in kor.items()), max(v[0] for k, v in kor.items())
    yY = min(v[1] for k, v in kor.items()), max(v[1] for k, v in kor.items())
    part1 = tile_loc(kor, xX[0], yY[0])[0] * tile_loc(kor, xX[0], yY[1])[0] * tile_loc(kor, xX[1], yY[0])[0] * tile_loc(kor, xX[1], yY[1])[0]
    print(part1)


    # Part 2
    mon = []
    with open('monster.txt', 'r') as file:
        for c, ln in enumerate(file):
            mon += [tuple(1 if i == '#' else 0 for i in ln.replace('\n', ''))]
    mon = pd.np.array(mon)
    ss = tuple(i-2 for i in data[next(iter(data))].shape)
    img = pd.np.zeros((ss[0] * (xX[1] - xX[0] + 1), ss[1] * (yY[1] - yY[0] + 1)), dtype = int)
    for i in range(xX[0], xX[1]+1):
        for j in range(yY[0], yY[1]+1):
            k = (lambda K = kor.items(), I = i, J = j: [k for k, v in K if v[0] == I and v[1] == J])()[0]
            mm = flip(pd.np.rot90(data[k], kor[k][2]), kor[k][3])[1:-1, 1:-1]
            img[(yY[1]-j)*ss[1]:(yY[1]-j+1)*ss[1], (i-xX[0])*ss[0]:(i-xX[0]+1)*ss[0]] = mm
    print('\n'.join([''.join('#' if i == 1 else '.' for i in l) for l in img]))
    mo = pd.np.where(mon)
    mm = 0
    for rot in range(4):
        for flp in range(4):
            im = img.copy()
            im = pd.np.rot90(im, rot)
            im = flip(im, flp)
            for i in range(im.shape[0] - mon.shape[0] +1 ):
                for j in range(im.shape[1] - mon.shape[1] + 1):
                    if (im[i:i+mon.shape[0], j:j+mon.shape[1]] == mon)[mo].all():
                        mm += 1
    print(int(img.sum() - mm / 2 * mon.sum()))

if __name__ == '__main__':
    main()
