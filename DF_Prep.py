import pandas as pd
import numpy as np
import pytz
import datetime
from datetime import date
from datetime import datetime, timedelta
import time

def data_prep(df):
 
    #EXTRACT INDEX TO COLUMN
    df.reset_index(inplace=True)

    #Column Rename
    df.columns = ['metric', 'value']

    # Split the first column on '_' and assign the values to new columns
    df[['larger_group', 'subgroup']] = df['metric'].str.split("_", expand=True,n=1)


    # Create new columns for the larger group and subgroup
    df['subgroup2'] = df['subgroup'].where(df['subgroup'].str.startswith("bookmakers"), None)
    df['bookmaker_name'] = df['subgroup2'].str.split("_").str[1]
    df['subgroup2'] = df['subgroup2'].str.replace('[\d_\s]','')
    df['h2h_spread'] = df['metric'].str.split("_")
    df['h2h_spread2'] = df['h2h_spread'].str[4] if len(df['h2h_spread'])>=5 else np.nan


    #TEAM 1 and TEAM 2
    df['Team1_2'] = df['h2h_spread'].str[6] if len(df['h2h_spread'])>=7 else np.nan


    #################EXTRACT THE ROWS WITH SPECIFIC IDENTIFIERS IN A SEPARATE DATAFRAME AND MERGE AT THE END
    # Create a boolean mask that is True for rows that contain the desired values in the column 'metric'
    mask1 = df['subgroup'].isin(['id','sport_key', 'sport_title', 'commence_time', 'home_team', 'away_team'])
    mask2 = df['subgroup2'].isin(['bookmakerskey', 'bookmakerstitle', 'bookmakerslastupdate'])
    mask3 = df['subgroup2'].isin(['bookmakersmarketskey','value'])

    # Use the mask to filter the rows
    df_filtered = df.loc[mask1]
    df_Book = df.loc[mask2]
    df_Moneyline = df.loc[mask3]

    df = df[~df['subgroup2'].isin(['bookmakerskey','bookmakerstitle','bookmakerslastupdate'])]
    df = df[~pd.isna(df['subgroup2'])]
    df.drop(columns=['h2h_spread'], inplace=True)


    df = df[~df['Team1_2'].isin(['update'])]
    df = df[~pd.isna(df['Team1_2'])]

    df["Team1_2"] = df["subgroup2"].astype(str) + " " + df["Team1_2"].astype(str)
    df=df.rename(columns={'Team1_2': 'Final_Team_column'})



    #This is the cross tab function:
    cross_tab = pd.crosstab(index=[df['larger_group'],df['bookmaker_name'],df['h2h_spread2']], columns=df['Final_Team_column'], values=df['value'], aggfunc='first')
    cross_tab_filtered = pd.crosstab(index=[df_filtered['larger_group']], columns=df_filtered['subgroup'], values=df_filtered['value'], aggfunc='first')
    cross_tab_Book = pd.crosstab(index=[df_Book['larger_group'],df_Book['bookmaker_name']], columns=df_Book['subgroup2'], values=df_Book['value'], aggfunc='first')
    crosstab_Moneyline = df_Moneyline[['value','larger_group','h2h_spread2','bookmaker_name']]

    #THIS IS WHERE WE WOULD REMERGE THE DATA (CROSS_TAB vs. CROSSTAB MONEYLINE)
    merged_df = pd.merge(cross_tab, crosstab_Moneyline, 
                        left_on=['larger_group', 'bookmaker_name', 'h2h_spread2'], 
                        right_on=['larger_group', 'bookmaker_name', 'h2h_spread2'], 
                        how='inner')

    merged_df = pd.merge(merged_df, cross_tab_Book, 
                        left_on=['larger_group', 'bookmaker_name'], 
                        right_on=['larger_group', 'bookmaker_name'], 
                        how='inner')


    merged_df = pd.merge(merged_df, cross_tab_filtered, 
                        left_on=['larger_group'], 
                        right_on=['larger_group'], 
                        how='inner')


    merged_df = merged_df.rename(columns={
    'id':'Event ID', 'sport_key':'sport_key','sport_title':'SPORT','bookmakerstitle':'Bookie Formal Name','bookmakerslastupdate':'Bookie Last Update', 
    'commence_time':'commence_time', 'home_team':'Home Team', 'away_team':'Away Team', 
    'bookmakersmarketsoutcomesname 0':'Team 1', 'bookmakersmarketsoutcomesname 1':'Team 2','value':'Bet Type', 
    'bookmakersmarketsoutcomespoint 0':'Spread 1', 'bookmakersmarketsoutcomespoint 1':'Spread 2','bookmakersmarketsoutcomesprice 0':'Moneyline 1', 'bookmakersmarketsoutcomesprice 1':'Moneyline 2',
    'larger_group':'Game Bracket', 'bookmaker_name':'bookmaker_name', 'h2h_spread2':'h2h_spread2','bookmakerskey':'Bookie'})


    merged_df = merged_df.drop(columns=['Game Bracket','bookmaker_name', 'h2h_spread2','Bookie'])
    merged_df = merged_df[['Event ID','sport_key','SPORT', 'Bookie Formal Name','Bookie Last Update','commence_time','Bet Type','Home Team', 'Away Team', 'Team 1','Team 2', 'Spread 1','Spread 2','Moneyline 1', 'Moneyline 2']]


    merged_df["Home Spread"] = np.where(merged_df["Team 1"] == merged_df["Home Team"], merged_df["Spread 1"], merged_df["Spread 2"])
    merged_df["Away Spread"] = np.where(merged_df["Team 2"] == merged_df["Away Team"], merged_df["Spread 2"], merged_df["Spread 1"])
    merged_df["Home Moneyline"] = np.where(merged_df["Team 1"] == merged_df["Home Team"], merged_df["Moneyline 1"], merged_df["Moneyline 2"])
    merged_df["Away Moneyline"] = np.where(merged_df["Team 2"] == merged_df["Away Team"], merged_df["Moneyline 2"], merged_df["Moneyline 1"])


    merged_df = merged_df.drop(columns=['Team 1','Team 2','Moneyline 1','Moneyline 2','Spread 1','Spread 2'])

    #COMMENCE TIME FIX
    merged_df['time_string'] = merged_df['commence_time']    
    merged_df['time'] = pd.to_datetime(merged_df['time_string'], format="%Y-%m-%dT%H:%M:%SZ")
    merged_df['utc_time'] = merged_df['time'].apply(lambda x: pytz.utc.localize(x))
    tz_nyc = pytz.timezone('America/New_York')
    merged_df['nyc_time'] = merged_df['utc_time'].apply(lambda x: x.astimezone(tz_nyc))


    # Get the current date and time in New York City
    merged_df['now'] = datetime.now(tz_nyc)

    #Get the Updated Time

    #Calculate the Difference


    # Format the current time and the converted time as 12-hour time strings
    merged_df['now_string'] = merged_df['now'].apply(lambda x: x.strftime("%Y-%m-%d %I:%M %p"))
    merged_df['nyc_time_string'] = merged_df['nyc_time'].apply(lambda x: x.strftime("%Y-%m-%d %I:%M %p"))
    merged_df["status"] = np.where(merged_df["now"] < merged_df["utc_time"], "Upcoming Game", "Live Game")


    merged_df = merged_df.drop(columns=['time','utc_time','nyc_time','now','time_string'])



    #NEW ADD ONS FOR 538 MERGE
    # Convert the 'commence_time' column to datetime format
    merged_df['commence_date'] = pd.to_datetime(merged_df['commence_time'])

    # Set the timezone to EST
    est = pytz.timezone('US/Eastern')

    # Convert the 'commence_time' column to EST
    merged_df['commence_date'] = merged_df['commence_date'].dt.tz_convert(est)

    # Format the date in the desired format
    merged_df['commence_date'] = merged_df['commence_date'].dt.strftime('%Y-%m-%d')


    #CONVERT BOOKIE UPDATE TO EST TIME
    merged_df['Bookie_Update'] = pd.to_datetime(merged_df['Bookie Last Update'], format="%Y-%m-%dT%H:%M:%SZ")
    merged_df['utc_time_bookie'] = merged_df['Bookie_Update'].apply(lambda x: pytz.utc.localize(x))
    merged_df['Bookie_Update'] = merged_df['utc_time_bookie'].apply(lambda x: x.astimezone(tz_nyc))
    merged_df['Bookie_Update'] = merged_df['Bookie_Update'].apply(lambda x: x.strftime("%Y-%m-%d %I:%M %p"))



    #LAST BOOKIE UPDATE
    merged_df['Bookie Last Update'] = pd.to_datetime(merged_df['Bookie Last Update'])
    merged_df['Bookie Last Update'] = merged_df['Bookie Last Update'].dt.tz_convert('US/Eastern').dt.floor('s')

    merged_df['current_time'] = datetime.now(pytz.timezone('US/Eastern'))

    #current_time = pd.datetime.now(pytz.timezone('US/Eastern'))
    merged_df['time_diff'] = merged_df['current_time'] - merged_df['Bookie Last Update']
    
    total_seconds = merged_df['time_diff'].dt.total_seconds()
    merged_df['minutes'], merged_df['seconds'] = divmod(total_seconds, 60)

    #print(merged_df.columns)

    
    #time_diff_min, time_diff_sec = divmod(time_diff.iloc[0].total_seconds(), 60)
    #merged_df['Time_Difference_minutes_seconds'] = f"{time_diff_min} minutes and {time_diff_sec} seconds"

    #print(merged_df[['time_diff','minutes', 'seconds','Bookie_Update','now_string']])



    return merged_df


#burger buns, Cheese, Onion and tomatoe

