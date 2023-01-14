from Settings import STATUS, LEAGUE, today_string, requests
import pandas as pd
from Flatten_Dict import flatten_json
import os
from dotenv import load_dotenv    

#Environment Variables Load
load_dotenv()



def process_metric_name(name):
    if 'results_' in name:
        return name[10:]  # keep the characters starting from the 11th position
    else:
        return name



def SportsFeed():

    url = "https://sportspage-feeds.p.rapidapi.com/games"

    querystring = {"status":STATUS, "league":LEAGUE, "date":today_string}

    headers = {
        "X-RapidAPI-Key": os.getenv('X-RapidAPI-Key'),
        "X-RapidAPI-Host": "sportspage-feeds.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    odds_json_sfl = response.json()

    dfs = pd.Series(flatten_json(odds_json_sfl)).to_frame()

    dfs.reset_index(inplace=True)
    dfs = dfs.rename(columns={'index': 'Metric',0:'Value'})

#    return dfs

    dfs['Metric'] = dfs['Metric'].apply(process_metric_name)

    dfs = dfs[dfs['Metric'].isin(['details_league', 'gameId', 'lastUpdated', 'scoreboard_currentPeriod', 
                                'scoreboard_periodTimeRemaining', 
                                'scoreboard_score_away', 'scoreboard_score_awayPeriods_0', 'scoreboard_score_awayPeriods_1', 'scoreboard_score_awayPeriods_2', 'scoreboard_score_awayPeriods_3', 
                                'scoreboard_score_home', 'scoreboard_score_homePeriods_0', 'scoreboard_score_homePeriods_1', 'scoreboard_score_homePeriods_2', 'scoreboard_score_homePeriods_3', 
                                'summary', 'teams_away_team', 'teams_home_team'])]

    dfs['recordID'] = 0
    counter = 0
    for index, row in dfs.iterrows():
        if row['Metric'] == 'summary':
            counter += 1
            dfs.loc[index, 'recordID'] = counter

    dfs['RecordID'] = (dfs['Metric'] == 'summary').cumsum()

    #create the cross tab
    dfs_pivoted = dfs.pivot_table(index='RecordID', columns='Metric', values='Value', aggfunc='first')

    column_names = ['details_league', 'gameId',   'lastUpdated', 'scoreboard_currentPeriod', 'scoreboard_periodTimeRemaining', 'scoreboard_score_away', 'scoreboard_score_awayPeriods_0', 
    'scoreboard_score_awayPeriods_1', 'scoreboard_score_awayPeriods_2', 'scoreboard_score_awayPeriods_3', 
    'scoreboard_score_home', 'scoreboard_score_homePeriods_0', 'scoreboard_score_homePeriods_1', 'scoreboard_score_homePeriods_2', 'scoreboard_score_homePeriods_3', 
    'summary', 'teams_away_team', 'teams_home_team']

    dfz = pd.DataFrame(columns=column_names)
    dfz = dfz.append(dfs_pivoted)
    #print(dfz.dtypes)

    dfz[['scoreboard_score_away', 'scoreboard_score_home']] = dfz[['scoreboard_score_away', 'scoreboard_score_home']].apply(pd.to_numeric)
    dfz = dfz[['lastUpdated','scoreboard_currentPeriod','scoreboard_periodTimeRemaining','teams_home_team', 'scoreboard_score_home', 'teams_away_team','scoreboard_score_away']]

    return dfz


#s = SportsFeed()
#print(s)




