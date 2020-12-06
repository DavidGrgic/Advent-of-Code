# -*- coding: utf-8 -*-
"""
@author: David Grgic
"""
import pandas as pd
import os, json
    
def main():
    _json = os.path.join(os.path.dirname(__file__), 'score.json')
    if not os.path.isfile(_json):
        return
    with open(_json) as f:
        sco = json.load(f)
    
    score = []
    for user_id, data in sco.get('members').items():
        name = data.get('name')
        score += (lambda N = name, D = data: [(int(user_id), N, int(d), int(p), int(w.get('get_star_ts'))) for d, v in D.get('completion_day_level').items() for p, w in v.items()])()
    score = pd.DataFrame(score, columns = ['ID', 'Name', 'Day', 'Part', 'Time'])
    score['UTC'] = score['Time'].astype('datetime64[s]')
    score['LT'] = pd.DatetimeIndex(score['UTC']).tz_localize('UTC').tz_convert('CET').tz_localize(None)
    score['LTstart'] = [pd.Timestamp('2020-12-01') + pd.Timedelta(days = v['Day']-1) + pd.Timedelta(hours = 6) for i, v in score.iterrows()]
    score['Minutes'] = (score['LT'] - score['LTstart']).astype('timedelta64[s]')/60

    score_id = score.groupby('ID')['Name'].first()

    # Day/Part statistic
    minutes = score.loc[(score['Day'] == 1) & (score['Part'] == 2), ['Name', 'Day', 'LT', 'Minutes']].sort_values('Minutes')

    # Name statistic 
    names = score.loc[score['Name'] == 'Blaž Peterlin'].sort_values(['Day', 'Part'])
    
    # AggregateByNames statistic
    score.loc[score['Part'] == 2].groupby('ID')[['Minutes']].mean().sort_values(['Minutes']).join(score_id)
    

if __name__ == '__main__':
    main()
