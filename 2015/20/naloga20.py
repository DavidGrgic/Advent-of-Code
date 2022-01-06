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


    # Part 1
    if True:
        house = 10**5
        presents = 0
        while presents < data:
#            if (house % 10**4) == 0: print(house)
            house += 1
            presents = 0
            for elv in factors(house):
                if (house % elv) == 0:
                    presents += 10 * elv
        print(f"A1: {house}")
          
    
    # Part 2

    print(f"A2: {0}")


if __name__ == '__main__':
    main()
