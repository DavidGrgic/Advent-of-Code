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

class Group:
    
    def __init__(self, definition: str):
        unit, temp = definition.split(' units each with ')
        self.unit = int(unit)
        point, temp = temp.split(' hit points ')
        self.point = int(point)
        self.immune = set()
        self.weak = set()
        if temp[0] == '(':
            imm_weak = temp[1:temp.find(')')]
            for iw in imm_weak.split('; '):
                match iw.split(' to '):
                    case 'weak', tmp:
                        self.weak |= set(tmp.split(', '))
                    case 'immune', tmp:
                        self.immune |= set(tmp.split(', '))
        temp = temp.split('with an attack that does ')[-1]
        damage, attack, *_, initiative = temp.split()
        self.attack = [attack, int(damage)]
        self.initiative = int(initiative)

    @property
    def power(self):
        return self.unit * self.attack[-1]

    def damage(self, target_group):
        effect = (2 if self.attack[0] in target_group.weak else 1) * (0 if self.attack[0] in target_group.immune else 1)
        return self.power * effect
    
    def boost(self, increase: int):
        self.attack[-1] += increase


def main():
    # Read
    army = None
    data = {}  # True is 'Immune' army, False is 'Infection' army
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            match ln.replace('\n', ''):
                case 'Immune System:':
                    army = True
                case 'Infection:':
                    army = False
                case '':
                    pass
                case x:
                    data.update({(army, len([k for k, _ in data if k == army])+1): Group(x)})

    def battle(dat):
        units = {k: v.unit for k, v in dat.items() if v.unit > 0}
        while all(sum(g.unit for (a,_),g in dat.items() if a == army) > 0 for army in {True, False}):
            # Target slection
            selection = [k for k,_ in sorted(dat.items(), key=lambda item: (item[-1].power, item[-1].initiative), reverse=True)]  # Target selection order
            target = {}
            for (army, idx) in selection:
                enemy = [(arm, i_) for (arm, i_), gru in sorted(dat.items(), key = lambda item: (dat[(army, idx)].damage(item[-1]), item[-1].power, item[-1].initiative), reverse=True)
                         if arm != army and (arm, i_) not in target.values() and dat[(army, idx)].damage(gru) > 0 and gru.unit > 0]
                target.update({(army, idx): enemy[0] if len(enemy) > 0 else None})
            # Attack
            attack = [k for k,_ in sorted(dat.items(), key=lambda item: item[-1].initiative, reverse=True)]  # Attack order
            for (army, idx) in attack:
                if (defending := target[(army, idx)]) is not None:
                    dat[defending].unit = max(0, dat[defending].unit - dat[(army, idx)].damage(dat[defending]) // dat[defending].point)
            #print({k: v.unit for k, v in dat.items() if v.unit > 0})
            if units == (units := {k: v.unit for k, v in dat.items() if v.unit > 0}):  # Nobody win 
                return
        return dat

    # Part 1
    if True:
        p1 = battle(copy.deepcopy(data))
        print(f"A1: {sum(g.unit for g in p1.values())}")

    # Part 2
    increase = [0, None]
    while any(i is None for i in increase) or (increase[-1] - increase[0]) > 1:
        inc = max(1, 2*increase[0]) if increase[-1] is None else (increase[-1] + increase[0]) // 2
        dat = copy.deepcopy(data)
        [g.boost(inc) for (a,_),g in dat.items() if a]
        res = battle(dat)
        if res is not None and (units := sum(g.unit for (a,_),g in res.items() if a)) > 0:
            increase[-1] = inc
            immune_units = units
        else:
            increase[0] = inc
    print(f"A2: {immune_units}")

if __name__ == '__main__':
    main()
