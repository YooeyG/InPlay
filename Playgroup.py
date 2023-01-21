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

from FiveThirtyEight import cross_tab

data_538 = cross_tab

print(s.os.getcwd())

#PICKLE LOGIC




# LOAD PICKLE
with open('data_oddsjam.pkl', 'rb') as f:
    df_subset = pickle.load(f)

print(df_subset)


#CONVERT COMMENCE DATE TO datetime64[ns]
data_538['Date'] = data_538['Date'].astype(str)
df_subset['commence_date'] = df_subset['commence_date'].astype(str)


print('DF_SUBSET')
print('############################')
print(df_subset['commence_date'].dtype)
print('############################')
print(data_538['Date'].dtype)
print('############################')


# #EXPORT TO EXCEL
#df_subset.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/subset.xlsx', sheet_name='final', index = True)
#data_538.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/cross_tab.xlsx', sheet_name='final', index = True)



df_m = pd.merge(df_subset, data_538,
    left_on=['commence_date', 'Home'], 
    right_on=['Date','Team_2'], 
    how='inner')


print('')
print('LETS GOOOO!!!!!!!!!!!!')
print(df_m)




