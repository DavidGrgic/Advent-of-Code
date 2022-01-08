# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd, numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
import mat

def main():

    me = [10, 0, 0, 250]  # hit points, damage, armor, mana
    boss = [13, 8, 0, None]  # hit points, damage, armor, mana
    boss = [14, 8, 0, None]  # hit points, damage, armor, mana
    me = [50, 0, 0, 500]  # hit points, damage, armor, mana
    boss = [51, 9, 0, None]  # hit points, damage, armor, mana

    # Read... (mana cost, damage, armor, hit heal, mana recharge, duration)
    spell = {'Missle': (53, None),
             'Drain': (73, None),
             'Shield': (113, 6),
             'Poison': (173, 6),
             'Recharge': (229, 5)}


    def turn(me, boss, hard = False, effect = {k: 0 for k, v in spell.items() if v[-1] is not None}, my_turn = True, globina = 0):
        if globina > globina_max:
            return set()

        if hard and my_turn:
            me[0] -= 1
            if me[0] <= 0:
                return {(False,)}

        for k, v in effect.items():
            if k == 'Shield' and v == 1:
                me[2] -= 7
            if k == 'Poison' and v > 0:
                boss[0] -= 3
            if k == 'Recharge' and v > 0:
                me[-1] += 101
        effect = {k: max(v-1,0) for k, v in effect.items()}
        if boss[0] <= 0:
            return {(True,)}

        if my_turn:
            spe = (lambda E = {k for k, v in effect.items() if v > 0}: {k: v for k, v in spell.items() if v[0] <= me[-1] and k not in E})()
            if len(spe) == 0:
                return set()

            res = set()
            for sp, ma in spe.items():
                mm = me.copy()
                bb = boss.copy()
                ee = effect.copy()
                mm[-1] -= ma[0]
                if sp == 'Missle':
                    bb[0] -= 4
                elif sp == 'Drain':
                    bb[0] -= 2
                    mm[0] += 2
                elif sp == 'Shield':
                    mm[2] += 7
                    ee[sp] += ma[-1]
                elif sp == 'Poison':
                    ee[sp] += ma[-1]
                elif sp == 'Recharge':
                    ee[sp] += ma[-1]
                if bb[0] <= 0:
                    res |= {(sp, True)}
                else:
                    re = turn(mm, bb, hard, ee, not my_turn, globina + 1)
                    res |= {(sp,) + r for r in re}
        else:
            me[0] -= max(boss[1] - me[2], 1)
            if me[0] <= 0:
                res = {(False,)}
            else:
                res = turn(me, boss, hard, effect, not my_turn, globina + 1)
        return res


    globina_max = 25  # Some games can be very long and since they consume a lot ob mana, we are not interested on them

    # Part 1
    if True:
        res1 = turn(me, boss)
        win1 = {r[:-1] for r in res1 if r[-1] == True}
        win_mana1 = {sum(spell[i][0] for i in w) for w in win1}
        print(f"A1: {min(win_mana1)}")


    # Part 2
    res2 = turn(me, boss, True)
    win2 = {r[:-1] for r in res2 if r[-1] == True}
    win_mana2 = {sum(spell[i][0] for i in w) for w in win2}
    print(f"A2: {min(win_mana2)}")


if __name__ == '__main__':
    main()
