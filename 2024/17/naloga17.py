# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys
import pandas as pd, numpy as np
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#from functools import cache   # @cache
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

class HexComp:
    
    def __init__(self, reg: dict, code):
        self.pointer = 0
        self.register = reg.copy()
        self.code = code.copy() if isinstance(code, dict) else {i: v for i, v in enumerate(code)}

    def literal(self):
        return self.code[self.pointer + 1]

    def combo(self):
        val = self.code[self.pointer + 1]
        if val <= 3:
            return val
        else:
            return self.register[chr(61+val)]

    def reset(self, reg):
        self.register.update({k: reg.get(k, 0) for k in self.register})
        self.pointer = 0

    def run(self):
        output = []
        while self.pointer in self.code:  
            match (opcode := self.code[self.pointer]):
                case 0 | 6 | 7:
                    self.register[{0: 'A', 6: 'B', 7: 'C'}[opcode]] = self.register['A'] // (2 ** self.combo() )
                    self.pointer += 2
                case 1:
                    self.register['B'] = self.register['B'] ^ self.literal()
                    self.pointer += 2
                case 2:
                    self.register['B'] = self.combo() % 8
                    self.pointer += 2
                case 3:
                    if self.register['A']:
                        self.pointer = self.literal()
                    else:
                        self.pointer += 2
                case 4:
                    self.register['B'] = self.register['B'] ^ self.register['C']
                    self.pointer += 2
                case 5:
                    output.append(self.combo() % 8)
                    self.pointer += 2
        return output

def main():
    # Read
    reg_ = {}
    code_ = []
    c_ = False
    with open('t1.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            if ln == '': # Nov blok podatkov
                c_ = True
                continue
            if c_:
                code_ += [int(i) for i in ln.lstrip('Program:').split(',')]
            else:
                r_, v_ = ln.lstrip('Register ').split(':')
                reg_.update({r_: int(v_)})

    # Part 1
    if True:
        comp = HexComp({'A': 0, 'B': 0, 'C': 9}, [2,6])
        comp.run()
        assert comp.register['B'] == 1
        comp = HexComp({'A': 10, 'B': 0, 'C': 0}, [5,0,5,1,5,4])
        assert comp.run() == [0, 1, 2]
        comp = HexComp({'A': 2024, 'B': 0, 'C': 0}, [0,1,5,4,3,0])
        assert comp.run() == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
        assert comp.register['A'] == 0
        comp = HexComp({'A': 0, 'B': 29, 'C': 0}, [1,7])
        comp.run()
        assert comp.register['B'] == 26
        comp = HexComp({'A': 0, 'B': 2024, 'C': 43690}, [4,0])
        comp.run()
        assert comp.register['B'] == 44354
        comp = HexComp(reg_, code_)
        p1 = comp.run()
        print(f"A1: {','.join(str(i) for i in p1)}")

    # Part 2
    a = 0
    hc = HexComp(reg_, code_)
    
    unpack = lambda x: sum(v * 8 ** i for i, v in enumerate(x[::-1]))


    # c = 0
    # a_ = [0]
    # while True:
    #     while True:
    #         hc.reset(reg_ | {'A': (a := unpack(a_))})
    #         out = hc.run()
    #         if out == code_[-len(out):]:
    #             break
    #         a_[0] += 1
    #     print(a, a_, c, out)
    #     if out == code_:
    #         break
    #     a_.insert(0,0)
    #     c += 1

    # c = 0
    # while True:
    #     while True:
    #         hc.reset(reg_ | {'A': a})
    #         out = hc.run()
    #         if out == code_[-len(out):]:
    #             break
    #         a += 1
    #     print(a, c, out)
    #     if out == code_:
    #         break
    #     a += 8**c
    #     c += 1
    
    """ Analyzing """
    if False:
        nxt_ending = lambda x: {k: v for k,v in res.items() if len(v) == len(x)+1 and v[-len(x):] == x}
        res = {}
        while True:
            hc.reset(reg_ | {'A': a})
            res.update({a: (out := hc.run())})
            if out == code_:
                break
            #print(a, out, end = '; ')
            a += 1
        tmp_ = []
        for k in range(len(code_)-1):
            print(tmp := nxt_ending(code_[-(k+1):]))  # For which next left outputs, remaining part match to the code_ ?
            tmp_.insert(0, (min(tmp) - unpack(tmp_)) // 8**k)
        print(tmp_)


    a_ = []
    while True:
        a = unpack(a_) + (a_[0] if len(a_) > 0 else 0)*8**len(a_)
        while True:
            hc.reset(reg_ | {'A': a})
            out = hc.run()
            if out == code_[-(len(a_)+1):]:
                if len(a_) > 0:
                    a_.insert(0, (a - unpack(a_)) // 8**len(a_))
                break
            a += 1
        if out == code_:
            break


    print(f"A2: {a}")

if __name__ == '__main__':
    main()
