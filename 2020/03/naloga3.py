# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
    
def main():
    x = pd.read_csv('data.csv', header = None).iloc[:,0]
    y = pd.DataFrame((lambda x = x: [tuple(j for j in df * int(7*x.shape[0] / len(x.iloc[0]) + 1)) for i, df in x.iteritems()])()) == '#'
    z = pd.Series([df.iloc[i*3] for i, df in y.iterrows()])
    print(z.sum())
    
    res = []
    for ij in [(1,1), (1,3), (1,5), (1,7), (2,1)]:
        res += [pd.Series((lambda y = y, ij = ij: [df.iloc[int(i/ij[0]*ij[1])] for i, df in y.iterrows() if i > 0 and (i % ij[0]) == 0])()).sum()]
    print(pd.np.prod(res))

if __name__ == '__main__':
    main()
