import Settings as s
import sys
import pandas as pd
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

# Open the file in binary mode
#with open('c.pkl', 'rb') as f:
#    c = pickle.load(f)
#Write in binary mode
#    pickle.dump(c, f)

   

n = 120
z = 0

q = n

while n > 0:
    if n < q:
        time.sleep(15)
    
    #ODDS JAM API
    c = JAM_API()

    #ODDS JAM DATA PREP#
    df = pd.Series(flatten_json(c)).to_frame()
    df_a = data_prep(df)

    #SPORTFEED DATA PREP#
    df_s = SportsFeed()
    #print(df_s)

    #TIMESTAMP
    tz_nyc = pytz.timezone('America/New_York')
    now = datetime.now(tz_nyc)
    now_string = now.strftime("%Y-%m-%d %I:%M %p")
    print(now_string)

    df_a["timestamp"] = now_string
    df_s["timestamp"] = now_string


    df_m = pd.merge(df_a, df_s, 
                        left_on=['Home Team','Away Team','timestamp'], 
                        right_on=['teams_home_team','teams_away_team','timestamp'], 
                        how='inner')


    # Subset the dataframe
    df_subset = df_m[(df_m["Bookie Formal Name"] == 'DraftKings') & (df_m["Bet Type"] == 'h2h')]

    # Select the specific columns
    df_subset.rename(columns={'scoreboard_currentPeriod': 'Quarter',
                            'scoreboard_periodTimeRemaining': 'Clock',
                            'teams_home_team': 'Home',
                            'scoreboard_score_home': 'Home Score',
                            'Home Moneyline': 'Home ML',
                            'teams_away_team': 'Away',
                            'scoreboard_score_away': 'Away Score',
                            'Away Moneyline': 'Away ML'}, inplace=True)

    df_subset = df_subset.loc[:, ['Quarter', 'Clock','Home', 'Home Score', 'Home ML','Away', 'Away Score','Away ML']]
    df_subset['Spread'] = df_subset['Home Score'] - df_subset['Away Score']
    print(df_subset)

#    print(df_subset.loc[:, ['scoreboard_currentPeriod', 'scoreboard_periodTimeRemaining',
#     'teams_home_team', 'scoreboard_score_home', 'Home Moneyline','teams_away_team', 
#    'scoreboard_score_away','Away Moneyline']])


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


# print('Open a file for writing in binary mode')


# #EXPORT TO EXCEL
df_livefeed.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/LiveTest.xlsx', sheet_name='final', index = True)
#df_a.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/DFprep.xlsx', sheet_name='final', index = True)
#df_s.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/DFsportsfeed.xlsx', sheet_name='final', index = True)
#df_m.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/FullDB.xlsx', sheet_name='final', index = True)


