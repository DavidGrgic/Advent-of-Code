# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import math, copy, os, sys, time
import pandas as pd, numpy as np
from joblib import Parallel, delayed
#from collections import Counter
#from fractions import Fraction
#from itertools import permutations, combinations, product
#import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
_img_map = {0: ' ', 1: '#'}; _img_print = lambda x: print('\n'+'\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]));
def _dict2img(x):
    offset = tuple(int(min(i[j] for i in x.keys())) for j in range(2))
    img = np.zeros(tuple(int(max(i[j] for i in x.keys())-offset[j])+1 for j in range(2))).astype(int)
    img[tuple(tuple(int(i[j]-offset[j]) for i in x.keys()) for j in range(2))] = list(x.values())
    return img

def blueprint(k, plan, tt = 24):
    
    def delaj(rob, inv, wsh = None , t = 0):
        if wsh == None:
            wsh = set(rob)
        t += 1
        if t > tt:
            return inv['g']
        dostopni = {kk for kk in rob.keys() if all(inv[k] >= v for k, v in plan[kk].items())}  # Katere robote lahkonaredimo, e.g. kateri so nam dostopni glede na material
        opcije = [(rob.copy(), {k: r + inv[k] for k, r in rob.items()}, set(rob) - dostopni)]  # Ne kupimo robota ampak samo produciramo rudo. To je smielno narediti samo če v naslednjem koraku delamo robota, ki ga nismo morali narediti v tem koraku
        for kk in dostopni & wsh:  # Kupimo katerega od robotov?
            if kk in prednost and rob[kk] >= prednost[kk]:   # Ce ze produciramo vec kk kot jo potrebuje najdrazji ostali robot za to rudo, potem nima smisla narediti robota kk
                continue
            _ro = {k: v + (1 if k == kk else 0) for k, v in rob.items()}
            _in = {k: r + inv[k] - plan[kk].get(k,0) for k, r in rob.items()} 
            opcije += [(_ro, _in, None)]
        res = 0
        for kk in opcije:
            go = delaj(*(kk + (t,)))
            res = max(go, res)
        return res
            
    rob = {'o': 1} | {k: 0 for k in {'c', 'b', 'g'}}
    inv = {k: 0 for k in {'o', 'c', 'b', 'g'}}
    prednost = {kk: max(v.get(kk, 0) for k, v in plan.items() if k != kk) for kk in {j for i in plan.values() for j in i}}
    return {k: delaj(rob, inv)}

def main():
    # Read
    data = {}
    with open('d.txt', 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '').replace('Blueprint ','')
            _dat = ln.split(':')
            da = _dat[1].replace(': ','').split('.')
            dat = {'o': {'o': int(da[0].replace('Each ore robot costs', '').replace('ore',''))}}
            dat.update({'c': {'o': int(da[1].replace('Each clay robot costs', '').replace('ore',''))}})
            d = da[2].replace('Each obsidian robot costs', '').replace('ore and' , ' ').replace('clay','').split()
            dat.update({'b': {'o': int(d[0]), 'c': int(d[1])}})
            d = da[3].replace('Each geode robot costs', '').replace('ore and' , ' ').replace('obsidian','').split()
            dat.update({'g': {'o': int(d[0]), 'b': int(d[1])}})
            data.update({int(_dat[0]): dat})

    # Part 1
    if True:
        p1 = Parallel(-1 if len(data) > 1 and sys.gettrace() is None else 1)(delayed(blueprint)(k, v) for k, v in data.items())
        p1 = {k: v for i in p1 for k, v in i.items()}
        print(f"A1: {sum(k * v for k, v in p1.items())}")

    # Part 2
    dat = {k: data[k] for k in range(1,4) if k in data}
    p2 = Parallel(-1 if len(data) > 1 and sys.gettrace() is None else 1)(delayed(blueprint)(k, v, 32) for k, v in dat.items())
    p2 = {k: v for i in p2 for k, v in i.items()}
    print(f"A2: {math.prod(p2.values())}")

if __name__ == '__main__':
    main()
