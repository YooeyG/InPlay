import Settings as s
import sys
print(sys.path)
import pandas as pd
import datetime
from datetime import date
from datetime import datetime, timedelta
import time

from Flatten_Dict import flatten_json
from DF_Prep import data_prep
import pytz
from  GameSchedules import commence
import GameSchedules

from Settings import api_key, API_KEY, SPORT, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT, requests
from OddsJam_API import JAM_API



n = 1
z = 1

while n > 0:
    if n < 5:
        time.sleep(5)
    
    c = JAM_API()
    df = pd.Series(flatten_json(c)).to_frame()
    a = data_prep(df)
    a['TimeStamp'] = datetime.now() 
    #print(len(a.columns.tolist()))

    #Commence Compare
    commence(c)

    #ACQUIRE PRE GAME OR START TIME OR LIVE GAME
    a['Gametime'] =     #ACQUIRE PRE GAME OR START TIME OR LIVE GAME
    #ACQUIRE PRE GAME OR START TIME OR LIVE GAME

    #Optional Print Loop
    t = a.iloc[0][11]
    print('Time Stamp',t)

    rslt_df = a.loc[a['Sports Book'] == 'DraftKings'] #Flexible choice
    rslt_dff = rslt_df.loc[rslt_df['Bet Type'] == 'h2h'] #Flexible choice
    rslt_dff = rslt_dff.loc[rslt_dff['Team 2'] == 'New York Knicks'] #Flexible choice
    print(rslt_dff[['TimeStamp','Team 1', 'Moneyline 1', 'Team 2', 'Moneyline 2']])
    #End Optional Print Loop


    if z == 1:
        #Create New DataFrame
        colnames = a.columns.tolist()
        newdf = pd.DataFrame(columns= colnames)
        newdf = newdf.append(a)
    else:
        newdf = newdf.append(a)

    n -= 1
    z += 1

    if n == 0:
        break
    print(n)
print('Loop ended.')
print(datetime.now())



