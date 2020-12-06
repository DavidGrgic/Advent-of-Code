# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
    
def main():
    data = ''
    with open('data.txt', 'r') as file:
        for c, l in enumerate(file):
            data += l

    data1 = data.replace('\n\n', '#').replace('\n', '')
    data1 = eval('["' +  data1.replace('#', '","') + '"]')
    dataset = [{j for j in i} for i in data1]
    dataset = [len(i) for i in dataset]
    print(sum(dataset))
    
    data2 = data.replace('\n\n', '")],[("').replace('\n', '"),("')
    data2 = eval('[("' + data2 + '")]')
    dataset = []
    for i in data2:
        dta = {i for i in 'abcdefghijklmnopqrstuvwxyz'}
        for j in i:
            dta &= {k for k in j}
        dataset += [dta]
    dataset = [len(i) for i in dataset]
    print(sum(dataset))


if __name__ == '__main__':
    main()
