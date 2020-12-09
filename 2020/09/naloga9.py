# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd

def main():
    
    # Read
    data = pd.read_csv('data.csv', header = None).iloc[:,0].astype(int)

    obseg = 25
    # Part 1
    i = obseg
    while True:
        ssub = data.iloc[i-obseg:i].values
        vsota = data.iloc[i]
        sub = ssub.reshape(-1,1) + ssub.reshape(1,-1)
        res = set()
        j = 0
        for su in sub:
            j += 1
            res |= set(su[j:])
        if vsota in res:
            i += 1
        else:
            break
    print(vsota)
    iskana = int(vsota)

    # Part 2
    ok = False
    for j in range(2,1000):
#        print(j)
        for i in range(j, 1000):
#            print(i)
            vsota = int(data.iloc[i-j:i].sum()) # int(data.iloc[i-j]) + int(data.iloc[i])
            if iskana == vsota:
                ok = True
                break
        if ok:
            break
    sub = data.iloc[i-j:i]
    print(sub.min()+ sub.max())

if __name__ == '__main__':
    main()
