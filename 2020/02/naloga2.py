# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
    
def main():
    x = pd.read_csv('data.csv', header = None).iloc[:,0]
    y = pd.DataFrame([tuple(v.replace('-', ' ').replace(':', '').split()) for i, v in x.iteritems()], columns = ['min', 'max', 'chr', 'pass']).astype({'min': int, 'max': int})
    y['freq'] = [len(tuple(c for c in df['pass'] if c == df['chr'])) for i, df in y.iterrows()]
    y['ok'] = (y['min'] <= y['freq']) & (y['freq'] <= y['max'])
    res = y.loc[y['ok']].shape[0]
    print(res)

    y['ok_pos'] = (pd.DataFrame([(df['pass'][df['min']-1] == df['chr'], df['pass'][df['max']-1] == df['chr']) for i, df in y.iterrows()]).sum(axis=1) == 1).values
    res = y.loc[y['ok_pos']].shape[0]
    print(res)

if __name__ == '__main__':
    main()
