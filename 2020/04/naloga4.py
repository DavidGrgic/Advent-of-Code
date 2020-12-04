# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import re

def main():
    
    def year4dig(sr, m, M):
        return len(sr) == 4 and (m <= eval(sr) <= M)
    
    def byr(sr):
        st = False
        if year4dig(sr, 1920, 2002):
            st = True
        return st
    
    def iyr(sr):
        st = False
        if year4dig(sr, 2010, 2020):
            st = True
        return st
    
    def eyr(sr):
        st = False
        if year4dig(sr, 2020, 2030):
            st = True
        return st
    
    def hgt(sr):
        st = False
        mM = {'cm': (150, 193), 'in': (59, 76)}.get(sr[-2:], (1, 0))
        try:
            if mM[0] <= eval(sr[:-2]) <= mM[1]:
                st = True
        except:
            pass
        return st
    
    def hcl(sr):
        st = False
        if sr[0] == '#' and len(sr[1:]) == 6 and bool(re.match('^[a-f0-9\.]+$', sr[1:])):
            st = True
        return st
    
    def ecl(sr):
        st = False
        if sr in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
            st = True
        return st
    
    def pid(sr):
        st = False
        if len(sr) == 9 and bool(re.match('^[0-9\.]+$', sr)):
            st = True
        return st
    
    
    line = ['']
    with open('data.txt', 'r') as file:
        for cnt, lin in enumerate(file):
            if lin != '\n':
                line[-1] = line[-1] + lin
            elif line[-1] != '':
                line += ['']
 #           line += [lin]
    
    line = [i.replace('\n', ',').replace(' ', ',') for i in line]
    line = [i[:-1] if i[-1] == ',' else i for i in line]
    data = [eval('{\"' + i.replace(':', '\":\"').replace(',', '\",\"') + '\"}') for i in line]
    
    req = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    kljuci = [{k:v for k,v in i.items() if k in req} for i in data]
    
    valid1 = (lambda K = kljuci, R = req: [i for i in K if len(i) >= len(R)])()
    print(len(valid1))

    valid2 = []
    for j, i in enumerate(valid1):
        chk = []
        for k, v in i.items():
           chk.append(eval('{0}("{1}")'.format(k,v)))
        if all(chk):
            valid2 += [i]
    print(len(valid2))
        

if __name__ == '__main__':
    main()
