# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    # Read
    data = {}
    with open('data.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            da = ln.split(' -> ')
            data.update({da[1]: da[0]})


    # Part 1
    global done
    done = {}
    if True:
        def calc(gate):
            global done
            if gate in done:
                return done[gate]
            if gate.isnumeric():
                res =  int(gate)
            else:
                ins = data[gate]
                if ins.isnumeric():
                    res = int(ins)
                elif ins[:3] == 'NOT':
                    res = 2**16 + ~ calc(ins[4:])
                elif ins.find('AND') > -1:
                    i = ins.find('AND')
                    res = calc(ins[:i-1]) & calc(ins[i+4:])
                elif ins.find('OR') > -1:
                    i = ins.find('OR')
                    res = calc(ins[:i-1]) | calc(ins[i+3:])
                elif ins.find('LSHIFT') > -1:
                    i = ins.find('LSHIFT')
                    res = (calc(ins[:i-1]) << int(ins[i+7:])) % 2**16
                elif ins.find('RSHIFT') > -1:
                    i = ins.find('RSHIFT')
                    res = calc(ins[:i-1]) >> int(ins[i+7:])
                else:
                    res = calc(ins)
            done[gate] = res
            return res

        res1 = calc('a')
        print(f"A1: {res1}")
          
    
    # Part 2
    data['b'] = str(res1)
    done = {}
    res2 = calc('a')
    print(f"A2: {res2}")


if __name__ == '__main__':
    main()
