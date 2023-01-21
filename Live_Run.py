import Settings as s
import sys
import pandas as pd
import numpy as np
import datetime
from datetime import date
from datetime import datetime, timedelta
import time

from Flatten_Dict import flatten_json
from DF_Prep import data_prep
import pytz
from SportsFeed_API import process_metric_name, SportsFeed

from Settings import API_KEY, SPORT, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT, requests
from OddsJam_API import JAM_API
import pickle

from FiveThirtyEight import cross_tab

data_538 = cross_tab

#PICKLE DUMP FILE - 'save' indicates on otehrwise it skips
retrieve = 'skip'

n = 1
z = 0

q = n

while n > 0:
    if n < q:
        time.sleep(1)
    
    #ODDS JAM API
    c = JAM_API()

    #ODDS JAM DATA PREP#
    df = pd.Series(flatten_json(c)).to_frame()
    df_a = data_prep(df)
 
    #SPORTFEED DATA PREP#
    df_s = SportsFeed()
 
    #CURRENT TIMESTAMP
    tz_nyc = pytz.timezone('America/New_York')
    now = datetime.now(tz_nyc)
    now_string = now.strftime("%Y-%m-%d %I:%M %p")
    print(now_string)

    df_a["timestamp"] = now_string
    df_s["timestamp"] = now_string
    df_a["now"] = now_string
 

    df_m = pd.merge(df_a, df_s, 
                        left_on=['Home Team','Away Team','timestamp'], 
                        right_on=['teams_home_team','teams_away_team','timestamp'], 
                        how='inner')


    # Subset the dataframe #THIS NEEDS TO BE FLEXIBLE#######################################################################
    df_subset = df_m[(df_m["Bookie Formal Name"] == 'DraftKings') & (df_m["Bet Type"] == 'h2h')]
    ########################################################################################################################

    # Select the specific columns
    df_subset.rename(columns={'scoreboard_currentPeriod': 'Quarter',
                            'scoreboard_periodTimeRemaining': 'Clock',
                            'teams_home_team': 'Home',
                            'scoreboard_score_home': 'Home Score',
                            'Home Moneyline': 'Home ML',
                            'teams_away_team': 'Away',
                            'scoreboard_score_away': 'Away Score',
                            'Away Moneyline': 'Away ML'}, inplace=True)

    df_subset = df_subset.loc[:, ['Bookie_Update','time_diff', 'minutes', 'seconds','commence_date','Quarter', 'Clock','Home', 'Home Score', 'Home ML','Away', 'Away Score','Away ML','now_string','nyc_time_string','now']]
    df_subset['Live Point Diff'] = df_subset['Home Score'] - df_subset['Away Score']

    
    #CALCULATE TIME DIFFERENTIAL BETWEEN API UPDATED AND ACTUAL TIME
    #SERIALIZE DATA AND MERGE INTO 538    
    if retrieve == 'save':
        with open('data_oddsjam.pkl', 'wb') as f:
            pickle.dump(df_subset, f)


    #CONVERT COMMENCE DATE TO datetime64[ns]
    data_538['Date'] = data_538['Date'].astype(str)
    df_subset['commence_date'] = df_subset['commence_date'].astype(str)


    df_m = pd.merge(df_subset, data_538,
        left_on=['commence_date', 'Home'], 
        right_on=['Date','Team_2'], 
        how='inner')

    
    df_m.rename(columns={'Score_1': 'Score_1',
                        'Score_2': 'Score_2',
                        'Spread_1': 'Away Spread - 538',
                        'Spread_2': 'Home Spread - 538',
                        'Prob_1': 'Away Prob',
                        'Prob_2': 'Home Prob',
                        }, inplace=True)

    df_m = df_m.drop(columns=['Game','Date','Team_1', 'Team_2','Score_1', 'Score_2'])
    

    #IDENTIFY FAVORITES
    df_m['Favorite'] = np.where(df_m['Home Prob'] > df_m['Away Prob'], df_m['Home'], df_m['Away'])

    #IDENTIFY TRIGGER
    df_m['Trigger'] = np.where((df_m['Favorite'] == df_m['Home']) & (df_m['Home ML'] > 100), 'Trigger', 
                      np.where((df_m['Favorite'] == df_m['Away']) & (df_m['Away ML'] > 100), 'Trigger', 
                      '-'))

    print(df_m.columns)
    #REORDER THE COLUMNS#
    df_m = df_m[['nyc_time_string','Quarter','Clock','Home','Home Prob','Home Spread - 538','Home ML','Away','Away Prob','Away Spread - 538','Away ML','now_string','Bookie_Update','minutes','seconds','Live Point Diff','Favorite','Trigger']]

    print(df_m)

    #INITIALIZE DATAFRAME
    if z == 0:
        df_livefeed = pd.DataFrame(columns=df_m.columns)
    df_livefeed = df_livefeed.append(df_m)


    n -= 1
    z += 1

    if n == 0:
        break

print("")
print('Loop ended.')
print("")


# #EXPORT TO EXCEL
df_livefeed.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/LiveTest.xlsx', sheet_name='final', index = True)


