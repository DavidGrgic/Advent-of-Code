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
    score['UTC0'] = [pd.Timestamp('2020-12-01') + pd.Timedelta(days = v['Day']-1) + pd.Timedelta(hours = 5) for i, v in score.iterrows()]
    score['Minutes'] = (score['UTC'] - score['UTC0']).astype('timedelta64[s]')/60
    score['LT'] = pd.DatetimeIndex(score['UTC']).tz_localize('UTC').tz_convert('CET').tz_localize(None)
    score['LTwkday'] = score['LT'].dt.dayofweek  # 0: Mon ... 6: Sun
    score['LThour'] = score['LT'].dt.hour
    

    score_id = score.groupby('ID')['Name'].first()

    # Day/Part statistic
    minutes = score.loc[(score['Day'] == 1) & (score['Part'] == 2), ['Name', 'Day', 'LT', 'Minutes']].sort_values('Minutes')

    # Name statistic 
    names = score.loc[score['Name'] == 'Blaž Peterlin'].sort_values(['Day', 'Part'])
    
    # AggregateByNames statistic
    score.loc[score['Part'] == 2].groupby('ID')[['Minutes']].mean().sort_values(['Minutes']).join(score_id)
    
    # Top listaper Day/Part
    top_no = 8
    top_lista = None
    for d in score['Day'].unique():
        tmp = pd.Series((lambda S = score, d=d, T = top_no: {p: '; '.join('{0} [{1}]'.format(v['Name'], round(v['Minutes'],1)) for i, v in S.loc[(S['Day'] == d) & (S['Part'] == p)].sort_values('Minutes').iloc[:T].iterrows()) for p in range(1,3)})()).to_frame(d).T
        top_lista = pd.concat([top_lista, tmp])
    top_lista.index.name = 'Day'
    top_lista.columns.name = 'Part'
    top_lista = top_lista.sort_index(axis = 0).sort_index(axis = 1)

    K = score['LTwkday'] <= 4
    h_wk= score.loc[K].groupby(['LThour', 'Part'])['ID'].count().unstack('Part')
    h_wkend= score.loc[~K].groupby(['LThour', 'Part'])['ID'].count().unstack('Part')
    h_week = pd.concat({'Mo-Fr': (100* h_wk / h_wk.sum()).round(1), 'Sa-Su': (100* h_wkend / h_wkend.sum()).round(1)}, axis = 1, names = ['Wkday'])
    h_week = pd.DataFrame(index = pd.Int64Index(range(24), name = h_week.index.name), columns = pd.MultiIndex.from_tuples([], names = h_week.columns.names)).join(h_week)

if __name__ == '__main__':
    main()
#   http://genisidt658:5008/