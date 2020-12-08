# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
    
def main():
    data = {}
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            key, val = ln.split(' bags contain ')
            if val[:14] == 'no other bags.':
                continue
            vals = val.split(', ')
            valss = [i[:i.find('bag')-1] for i in vals]
            tmp = {}
            for i in valss:
                k = i.find(' ')
                tmp.update({i[k+1:]: int(i[:k])})
            data.update({key: tmp})

    data1 = {k: set(v) for k, v in data.items()}
    bags1 = {'shiny gold'}
    bags1_sz = 1
    while True:
        bags1 |= (lambda D = data1, B = bags1: {k for k, v in D.items() if any([i in v for i in B])})()
        if len(bags1) == bags1_sz:
            break
        else:
            bags1_sz = len(bags1)
    print(len(bags1)-1)

    bags2 = [['shiny gold']]
    while True:
        tmp = []
        for i in bags2[len(bags2)-1]:
            tt = data.get(i, {})
            tmp += [j for i in [[k]*v for k, v in tt.items()] for j in i]
        if len(tmp) == 0:
            break
        bags2 += [tmp]
    bags2 = [j for i in bags2 for j in i]
    print(len(bags2)-1)


if __name__ == '__main__':
    main()
