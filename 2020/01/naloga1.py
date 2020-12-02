# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
    
def main():
    x = pd.read_csv('data.csv', header = None)#.iloc[:,0:0]
    y = x.values + x.T.values
    ind = pd.np.where(y == 2020)[0]
    res = x.iloc[ind].prod().iloc[0]
    print(res)
    
    y = x.values
    y = y.reshape((-1,1,1)) + y.reshape((1,-1,1)) + y.reshape((1,1,-1))
    ind = pd.np.unique(pd.np.where(y == 2020)[0])
    res = x.iloc[ind].prod().iloc[0]
    print(res)

if __name__ == '__main__':
    main()
