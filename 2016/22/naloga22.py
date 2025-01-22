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
import networkx as nx   # G = nx.DiGraph(); G.add_edges_from([('Start', 'B'), ('B', 'C'), ('Start', 'C'), ('C', 'End')]); nx.shortest_path(G, 'Start', 'End'); G.add_weighted_edges_from([('Start', 'B', 1.7), ('B', 'C', 0.6), ('Start', 'C', 2.9), ('C', 'End', 0.2)]); nx.shortest_path(G, 'Start', 'End', 'weight')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
def plot(data, mapper: dict = {0: '.', 1: '#'}, default: dict = {set: 1, dict: 0}):
    if isinstance(data, set):
        data = {k: default[set] for k in data}
    if isinstance(data, dict):
        offset = tuple(int(min(i[j] for i in data.keys())) for j in range(2))
        img = np.zeros(tuple(int(max(i[j] for i in data.keys())-offset[j])+1 for j in range(2))).astype(int) + default[dict]
        img[tuple(tuple(int(i[j]-offset[j]) for i in data.keys()) for j in range(2))] = list(data.values())
        data = img
    print('\n'+'\n'.join([''.join(mapper.get(i,'?') for i in j) for j in data]))

def main():
    # Read
    data = {}
    with open('d.txt', 'r') as file:
        for i, ln in enumerate(file):
            if i < 2:
                continue
            xy, *sua, _ = ln.replace('\n', '').split()
            data.update({tuple(int(i[1:]) for i in xy.split('-')[-2:])[::-1]:
                         [int(i[:-1]) for i in sua]})

    plus = lambda a,b: tuple(i+j for i,j in zip(a,b))
    distance = lambda a,b: sum(abs(i-j) for i,j in zip(a,b))
                
    # Part 1
    if True:
        p1 = set()
        for i, a in data.items():
            for j, b in data.items():
                if i != j and a[1] != 0 and a[1] <= b[2]:
                    p1.add((i,j))
        print(f"A1: {len(p1)}")

    # Part 2
    show = False
    # Find nodes small enougt to fit in any other such small node and than work with just that nodes.
    access = (0,0)
    node = sorted(data.items(), key=lambda i: (i[1][1], -i[1][0]))
    assert node[0][1][1] == 0, "One node should be empty."
    empty_ = node[0][0]
    goal_ = (0, max(i[0][1] for i in node))
    node = {node[i][0] for i in range(len(node)) if node[i][1][1] <= min(s for _,(s,*_) in node[:i+1])}
    assert access in node, "Access node should be one of 'movable nodes'."
    assert goal_ in node, "Goal node should be one of 'movable nodes'."
    
    neighbour = lambda yx: {yx_ for d in {(1,0), (-1,0), (0,1), (0,-1)} if (yx_ := plus(yx, d)) in node}  # All node neighbours, e.g. directly attached nodes, with used value
    
    def plt(position):  # To help visualize current state, position is tuple, first component is node of goal data, second is empty node
        ret = {k: 1 for k in node} | {k: i+2 for i, k in enumerate(position)}
        plot(ret, {0: '#', 1: '.', 2: 'G', 3: '_'})
    
    # Frst move empty space close to goal data.
    edge = [(yx, yx_) for yx in node for d in {(1,0), (0,1)} if (yx_ := plus(yx, d)) in node and goal_ not in {yx, yx_}]
    G = nx.Graph()
    G.add_edges_from(edge)
    path = []
    for nn in neighbour(goal_):
        path += [nx.shortest_path(G, empty_, nn)]
    path = {l-1: {(goal_, i[-1]) for i in path if len(i) == l} for l in {len(i) for i in path}}  # key is time it took to tkae empty at that position, value is tuple of goal and empty node, eg. state
    
    # Second, use Breadth First Search (BFS) to move goal data to access node. State is tuple of goal and empty node
    goal_treashold = sum(max(i[j] for i in node) for j in range(2))   # To speed up BFS, keep only states, where goal has moved more or equal away from access node. Value has to be 0 or greater
    empty_treashold = sum(max(i[j] for i in node) for j in range(2))  # To speed up BFS, keep only states, where empty stayed close to goal with this margin. Value has to be 2 or greater
    p2 = []
    for tt, state_ in path.items():
        t = tt
        best = distance(goal_, access); archive = set()
        while True:
            archive |= state_
            t += 1
            state = set()
            for pos_ in state_:
                for nn in neighbour(pos_[1]):
                    if distance(pos_[0], nn) > empty_treashold:
                        continue
                    pos = pos_[::-1] if nn in pos_ else (pos_[0], nn)  # Swap
                    if pos not in archive and (dist := distance(pos[0], access)) <= best + goal_treashold:
                        state.add(pos)
                        if dist < best:
                            best = dist
                            if show:
                                plt(pos)
            if show:
                print(f"At {t}, number of states: {len(state)}, best is {best} away.")
            if len(state) == 0:
                t = float('inf')
                break
            if any(pos[0] == access for pos in state) or t > 300:
                break
            state_ = state
        p2.append(t)
    print(f"A2: {min(p2)}")

if __name__ == '__main__':
    main()
