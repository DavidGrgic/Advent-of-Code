# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd

def main():
    
    # Read
    data = [19,0,5,1,10,13]

    # Part 1
    dta = pd.Series(data)
    if True:
        while dta.shape[0] < 2020:
            K = dta.iloc[:-1] == dta.iloc[-1]
            if not K.any():
                x = 0
            else:
                x = dta.shape[0] - pd.np.where(K)[0][-1] -1
            dta = dta.append(pd.Series([x]))
        print(dta.iloc[-1])


    # Part 2
    l = data[-1]
    i = len(data)
    data = {v:(i, i) for i, v in enumerate(data)}
    while i < 30000000:
        if l in data and data.get(l)[1] < i-1:
            l = i - data[l][1] - 1
        else:
            l = 0
        data.update({l:(i, data.get(l, [10**10])[0])})
        i+=1
        # if (i % 10**5 ) == 0:
        #     print(i/(10**6))
    print(l)

if __name__ == '__main__':
    main()
