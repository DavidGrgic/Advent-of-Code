# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
from collections import Counter
from fractions import Fraction
from itertools import permutations, combinations, product
from dataclasses import dataclass, field
import os, sys, copy, math
import networkx as nx
_img_map = {0: '.', 1: '#'}; _img_print = lambda x: print('\n'.join([''.join(_img_map.get(i,'?') for i in j) for j in x]))


class IntCode():
    
    def __init__(self, code: list[int], input_ = None):
        self.pointer = 0
        self.base = 0
        assert isinstance(code, (list, tuple, dict))
        self.code_ = code.copy() if isinstance(code, dict) else {i: int(v) for i, v in enumerate(code)}
        self.input_ = [] if input_ is None else [[int(i) for i in input_]]
        self.input_consumed = []
        self.output_ = []
        
    
    def __repr__(self):
        return f"pointer={self.pointer}: base={self.base}\n{','.join(str(i) for i in self.code())}"
    
    def run(self, input_ = None):
        address = lambda offset: self.code_[self.pointer+offset] + (self.base if mode[offset-1] == 2 else 0)
        value = lambda offset: self.code_.get(self.pointer+offset, 0) if mode[offset-1] == 1 else self.code_.get(address(offset), 0)
        if input_ is not None:
            self.input_add(input_)
        while True:
            instruction = self.code_[self.pointer]
            mode = [int(i) for i in str(instruction // 100).rjust(3,'0')[::-1]]
            match instruction % 100:
                case 99:
                    self.pointer += 1
                    status = None
                    break
                case 1:  # Add by position
                    self.code_[address(3)] = value(1) + value(2)
                    self.pointer += 4
                case 2:  # Multiply by position
                    self.code_[address(3)] = value(1) * value(2)
                    self.pointer += 4
                case 3:
                    if len(self.input_) > 0:
                        in_ = self.input_.pop(0)
                        self.code_[address(1)] = in_
                        self.input_consumed.append(in_)
                        self.pointer += 2
                    else:
                        status = True
                        break
                case 4:
                    self.output_.append(value(1))
                    self.pointer += 2
                case 5:
                    if value(1) != 0:
                        self.pointer = value(2)
                    else:
                        self.pointer += 3
                case 6:
                    if value(1) == 0:
                        self.pointer = value(2)
                    else:
                        self.pointer += 3
                case 7:
                    self.code_[address(3)] = 1 if value(1) < value(2) else 0
                    self.pointer += 4
                case 8:
                    self.code_[address(3)] = 1 if value(1) == value(2) else 0
                    self.pointer += 4
                case 9:
                    self.base += value(1)
                    self.pointer += 2
                case _:
                    raise RuntimeError('Something went wrong.')
        return status  # None: Program terminated, True: Waiting for input

    def input_add(self, input_):
        self.input_.extend([int(i) for i in input_] if hasattr(input_, '__iter__') else [int(input_)])
        
    def output(self, consume = True):
        ret = self.output_.copy()
        if consume:
            self.output_ = []
        return ret

    def code(self):
        return list(i[1] for i in sorted(self.code_.items()))

@dataclass
class Room:
    description: str
    door: dict = field(default_factory = lambda: {})
    inventory: set = field(default_factory = lambda: set())
    password: bool = False
    
def read(filename):
    with open(filename, 'r') as file:
        for c, ln in enumerate(file):
            ln = ln.replace('\n', '')
            data = {i: int(v) for i, v in enumerate(ln.split(','))}
    return data

def main():
    data = read('d.txt')

    def find(output, start: str, end: str):
        idx_s = output.find(start)
        if idx_s < 0:
            return ''
        else:
            idx_s += len(start)
        idx_e = output[idx_s:].find(end)
        if idx_e < 0:
            idx_e = None
        else:
            idx_e += idx_s
        return output[idx_s:idx_e]
    
    def parse_room(output: str):
        room = find(output, '== ', ' ==\n')
        desc = find(output, ' ==\n', '\n\n')
        door = {k: None for k in find(output, '\n\nDoors here lead:\n- ', '\n\n').split('\n- ')}
        inv = set(find(output, '\n\nItems here:\n- ', '\n\n').split('\n- ')) - {''}
        return room, desc, door, inv

    def parse_inv(output: str):
        inv = set(find(output, '\n\nItems in your inventory:\n- ', '\n\n').split('\n- ')) - {''}
        return inv
        
    # Part 1
    danger = {'infinite loop'}  # Collection of dangerous invertory ('infinite loop' is goten via debuging)
    light = []; heavy = []
    direction = ({'north', 'south'}, {'east', 'west'})
    play = explore = True
    while play:  # Play game
        room = {}  # Collection of rooms discovered
        comp = IntCode(data)
        next_dir = None
        take = set()
        instruction = None
        while comp.run([ord(i) for i in instruction] + [10] if isinstance(instruction, str) else instruction):
            #print(''.join(chr(i) for i in comp.output(False)))
            output = (''.join(chr(i) for i in comp.output(False))).split('\n\nCommand?')[-2]
            if len(take) > 0:
                inv = instruction.removeprefix('take ')
                assert output == f"\n\nYou take the {inv}."
                take -= {inv}
                if len(take) > 0:
                    instruction = f"take {next(iter(take))}"
                    continue
            elif output.endswith("You can't move!!"):
                inv = next(iter({i for r, v in room.items() for i in v.inventory if output.find(i) >= 0}))
                danger |= {inv}
                break
            else:
                current_room, des, dor, inv = parse_room(output)
                if current_room not in room:
                    room[current_room] = Room(des, dor)
                room[current_room].inventory = inv
                if isinstance(next_dir, tuple):
                    room[next_dir[1]].door[next_dir[0]] = current_room
                    room[current_room].door[next(iter(next(iter(d for d in direction if next_dir[0] in d)) - {next_dir[0]}))] = next_dir[1]
                # we might be automatically pushed back into some other room
                if len(out := output.split('\n\n\n\n')) > 2:
                    room[current_room].password = True
                    current_room, _, _, inv = parse_room(out[-1])
                    room[current_room].inventory = inv
                # Collect items
                take = room[current_room].inventory - danger
                if len(take) > 0:
                    instruction = f"take {next(iter(take))}"
                    continue
                else:
                    take = set()
            # Explore directions in current room
            next_dir = {k for k, v in room[current_room].door.items() if v is None}
            if len(next_dir) > 0:
                next_dir = next(iter(next_dir)), current_room
                instruction = next_dir[0]
                continue
            else:
                next_dir = None
            # Explore directions elsewhere
            graf = nx.Graph()
            graf.add_edges_from({tuple(sorted((r, r_))) for r, v in room.items() for d, r_ in v.door.items() if r_ is not None})
            pot = []
            target = {r for r, v in room.items() for _, r_ in v.door.items() if r_ is None}
            if len(target) == 0:
                target = {r for r, v in room.items() if v.password}
                explore = False
            for tar in target:
                pot.append(tuple(nx.shortest_path(graf, current_room, tar)))
            if len(pot) > 0:
                pot = sorted(pot, key = lambda x: len(x))[0]
                if not explore:
                    pot = pot[:-1]
                    if len(pot) <= 1:
                        break
                pot = [[d for d, r_ in room[r].door.items() if r_ == pot[i+1]][0] for i, r in enumerate(pot[:-1])]
                instruction = chr(10).join(pot)
        if instruction.startswith("take "):
            danger |= {instruction.removeprefix('take ')}
            continue
        if explore:
            continue
        # Try to enter into security area
        instruction = 'inv'
        comp.run([ord(i) for i in instruction] + [10] if isinstance(instruction, str) else instruction)
        output = (''.join(chr(i) for i in comp.output(False))).split('\n\nCommand?')[-2]
        inventory = parse_inv(output)
        for inv in inventory:
            instruction = f"drop {inv}"
            comp.run([ord(i) for i in instruction] + [10] if isinstance(instruction, str) else instruction)
        num_item = 1
        while play and num_item <= len(inventory):
            for inv in [i for i in combinations(inventory, num_item) if not any(len(h - set(i))==0 for h in heavy)]:
                instruction = chr(10).join(f"take {i}" for i in inv) + f"{chr(10)}north"
                if not comp.run([ord(i) for i in instruction] + [10] if isinstance(instruction, str) else instruction):
                    play = False
                    break
                output = (''.join(chr(i) for i in comp.output(False))).split('\n\nCommand?')[-2]
                match find(output, 'Alert! Droids on this ship are ', ' than the detected value!'):
                    case 'heavier':
                        light += [set(inv)]
                    case 'lighter':
                        heavy += [set(inv)]
                    case _:
                        play = False
                        break
                instruction = chr(10).join(f"drop {i}" for i in inv)
                comp.run([ord(i) for i in instruction] + [10] if isinstance(instruction, str) else instruction)
            num_item += 1
    output = (''.join(chr(i) for i in comp.output(False))).split('\n\nCommand?')[-1]        
    password = find(output, 'You should be able to get in by typing ', ' on the keypad at the main airlock.')
    print(f"A1: {password}")

if __name__ == '__main__':
    main()
