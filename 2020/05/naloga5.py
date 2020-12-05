# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
    
def main():
    x = pd.read_csv('data.csv', header = None).iloc[:,0]
    x = pd.DataFrame([tuple(j for j in v) for i, v in x.iteritems()])
    rw = x.iloc[:, :7] == 'B'
    rw = pd.Series([int(sum(tuple(2**(v.shape[0]-1-j) for j, w in v.iteritems() if w))) for i, v in rw.iterrows()])
    si = x.iloc[:, 7:] == 'R'
    si = pd.Series([int(sum(tuple(2**(v.shape[0]+6-j) for j, w in v.iteritems() if w))) for i, v in si.iterrows()])
    bp = rw.to_frame('R').join(si.to_frame('S'))
    bp['ID'] = bp['R'] * 8 + bp['S']
    print(bp['ID'].max())
    
    m = (bp['R'].min()+1) * 8
    M = bp['R'].max() * 8
    se = {int(v) for i, v in bp.loc[(bp['ID'] >= m) & (bp['ID'] <= M)]['ID'].iteritems()}
    res = (lambda se = se, m=m, M=M: [i for i in range(m,M) if i not in se])()
    print(res)

if __name__ == '__main__':
    main()
