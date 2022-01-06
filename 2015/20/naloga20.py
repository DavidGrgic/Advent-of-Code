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
    data = 33100000


    def factors(n):
        # https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
        return set(x for tup in ([i, n//i] for i in range(1, int(n**0.5)+1) if n % i == 0) for x in tup)


    def obiski(per_house, per_elve = None, house = 0):
        presents = 0
        while presents < data:
            house += 1
            presents = 0
            for elve in factors(house):
                if per_elve is None or (house / elve) <= per_elve:
                    presents += per_house * elve
        return house


    # Part 1
    if True:
        house = obiski(10)
        print(f"A1: {house}")
          
    
    # Part 2
    house = obiski(11, 50)
    print(f"A2: {house}")


if __name__ == '__main__':
    main()
