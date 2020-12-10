# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd

def main():
    
    # Read
    data = pd.read_csv('data.csv', header = None).iloc[:,0].astype(int)

    # Part 1
    d1 = data.copy().append(pd.Series([0,data.max()+3])).reset_index(drop = True).sort_values()
    d1 = d1.diff().to_frame('V')
    d1['C'] = 1
    d1 = d1.iloc[1:].astype(int).groupby('V').count()
    print(d1.loc[{1,3}].prod().iloc[0])


    # Part 2
    d2 = data.copy().append(pd.Series([0,data.max()+3])).reset_index(drop = True).sort_values()
    d2 = d2.reset_index(drop = True)
    dd = [1]
    for i in range(1, d2.shape[0]):
        ddd = 0#-1
        k = 0
        for j in range(1,4):
            if i-j >= 0 and (d2.iloc[i] - d2.iloc[i-j]) <= 3:
                ddd += dd[i-j] + 1
                k+=1
        dd += [ddd-k]
    print(dd[-1])

if __name__ == '__main__':
    main()
