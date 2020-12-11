# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd

def main():
    
    # Read
    data = pd.read_csv('data.csv', header = None).iloc[:,0]
    dd = []
    for i, r in data.iteritems():
        ddd = []
        for j in r:
            ddd += [1 if j == 'L' else -1]
        dd += [ddd]
    data = pd.DataFrame(dd).values

    # Part 1
    if True:
        dd = data.copy()
        mode = 1
        while True:
            mode *= -1
            dd_ = dd.copy()
            for i, r in enumerate(dd):
                for j, v in enumerate(r):
                    sosedje = dd[max(i-1,0):i+2, max(j-1,0):j+2]
                    sosedje = sosedje.reshape(-1)
                    sosedje = pd.np.append(sosedje, pd.np.array([0]*(9-sosedje.shape[0])))
                    if mode == -1 and dd[i,j] == 1: # odhajajo
                        if (sosedje == 1).sum() >= 5:
                            dd_[i,j] = 0
                    if mode == 1 and dd[i,j] == 0: # prihajajo
                        if (sosedje != 1).sum() == 9:
                            dd_[i,j] = 1
            print((dd_ == 1).sum())
            if (dd == dd_).all():
                break
            else:
                dd = dd_.copy()
        print('Part1: {}\n'.format((dd_ == 1).sum()))

    # Part 2
    if True:
        dd = data.copy()
        mode = 1
        rr = pd.np.array(range(dd.shape[1]))
        while True:
            mode *= -1
            dd_ = dd.copy()
            for i, r in enumerate(dd):
                for j, v in enumerate(r):
                    rw = dd[i,:].reshape(-1)
                    cl = dd[:,j].reshape(-1)
                    rr_ = rr + i -j
                    K = (rr_ >= 0) & (rr_ < dd.shape[0])
                    ul = pd.np.zeros_like(rr)-1
                    ul[K] = dd[rr_[K], rr[K]]
                    rr_ = -rr + i +j
                    K = (rr_ >= 0) & (rr_ < dd.shape[0])
                    lu = pd.np.zeros_like(rr)-1
                    lu[K] = dd[rr_[K], rr[K]]
                    sosedje = 0
                    for v, k in [(rw, j), (cl, i), (ul, j), (lu, j)]:
                        t = v[:k][v[:k] != -1]
                        if t.shape[0] > 0 and t[-1] == 1:
                            sosedje += 1
                        t = v[k+1:][v[k+1:] != -1]
                        if t.shape[0] > 0 and t[0] == 1:
                            sosedje += 1
                    if mode == -1 and dd[i,j] == 1: # odhajajo
                        if sosedje >= 5:
                            dd_[i,j] = 0
                    if mode == 1 and dd[i,j] == 0: # prihajajo
                        if sosedje == 0:
                            dd_[i,j] = 1
            print((dd_ == 1).sum())
            if (dd == dd_).all():
                break
            else:
                dd = dd_.copy()
        print('Part2: {}\n'.format((dd_ == 1).sum()))

if __name__ == '__main__':
    main()
