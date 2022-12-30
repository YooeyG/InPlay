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
from  GameSchedules import commence
import GameSchedules

from Settings import api_key, API_KEY, SPORT, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT, requests
from OddsJam_API import JAM_API
import pickle

# Open the file in binary mode
#with open('c.pkl', 'rb') as f:
#    c = pickle.load(f)
#Write in binary mode
#    pickle.dump(c, f)



#NEXT STEP IS TO CREATE THE LOOP TO APPEND
#LOGIC TO START GRAPHING A GAME
   

n = 4
z = 0

while n > 0:
    if n < 5:
        time.sleep(1)
    
    #serialization pickle file
    #c = JAM_API()
    with open('c.pkl', 'rb') as f:
        c = pickle.load(f)
        #print(c)

    df = pd.Series(flatten_json(c)).to_frame()
    df_a = data_prep(df)

    #ACQUIRE PRE GAME OR START TIME OR LIVE GAME - LISTS LIVE TIME ALSO
    commence_df = commence(c)
    #print(commence_df)

    rslt_df = df_a.loc[df_a['Sports Book'] == 'DraftKings'] #Flexible choice
    rslt_dff = rslt_df.loc[rslt_df['Bet Type'] == 'h2h'] #Flexible choice
    rslt_dff = rslt_dff[['Sports Book','Value','Team 1', 'Moneyline 1', 'Team 2', 'Moneyline 2']]
        
    result_df = commence_df.merge(rslt_dff, on='Value', how='inner')
    print(result_df)

    #INITIALIZE DATAFRAME
    if z == 0:
        df_livefeed = pd.DataFrame(columns=result_df.columns)
    
    df_livefeed = df_livefeed.append(result_df)

    n -= 1
    z += 1

    if n == 0:
        break

print("")
print('Loop ended.')
print("")


print('Open a file for writing in binary mode')

with open('df_livefeed.pkl', 'wb') as f:
    pickle.dump(df_livefeed, f)


