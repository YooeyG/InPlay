#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:07:49 2022

@author: ryanmurphy
"""
#SOURCE: https://rapidapi.com/SportspageFeeds/api/sportspage-feeds
#https://api.sportspagefeeds.com/teams?league=NFL&conference=AFC



import requests
import pandas as pd
from datetime import datetime




#STATUS OPTIONS: 
#scheduled, in progress, final, canceled, delayed
STATUS = 'in progress'

#League Options
#NFL, NBA, MLB, NHL, NCAAF, or NCAAB
LEAGUE = 'NBA'

#DATE
today = datetime.now()
today_string = today.strftime("%Y-%m-%d")



url = "https://sportspage-feeds.p.rapidapi.com/games"

#ORIGINAL WORKING EXAMPLE
#querystring = {"status":"scheduled","league":"NFL","date":"2022-11-20"}

#SPECIFIC LEAGE
querystring = {"status":STATUS, "league":LEAGUE, "date":today_string}

#All Games
querystring = {"status":STATUS, "date":today_string}


#SPECIFIC LEAGUE AND DATE
querystring = {"status":'final',"league":LEAGUE,"date":"2022-12-29"}


headers = {
	"X-RapidAPI-Key": "c56058d507mshe08ef7f5a175d0cp194176jsn8122f72c24d7",
	"X-RapidAPI-Host": "sportspage-feeds.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
#print(response.text)

odds_json_sfl = response.json()


def flatten_json(nested_json):
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


dfs = pd.Series(flatten_json(odds_json_sfl)).to_frame()

dfs.reset_index(inplace=True)
dfs = dfs.rename(columns={'index': 'Metric',0:'Value'})


def process_metric_name(name):
    if 'results_' in name:
        return name[10:]  # keep the characters starting from the 11th position
    else:
        return name

dfs['Metric'] = dfs['Metric'].apply(process_metric_name)



dfs = dfs[dfs['Metric'].isin(['details_league', 'gameId', 'lastUpdated', 
                              'scoreboard_currentPeriod', 
                              'scoreboard_periodTimeRemaining', 
                              'scoreboard_score_away', 
                              'scoreboard_score_awayPeriods_0', 
                              'scoreboard_score_awayPeriods_1', 
                              'scoreboard_score_awayPeriods_2', 
                              'scoreboard_score_awayPeriods_3', 
                              'scoreboard_score_home', 
                              'scoreboard_score_homePeriods_0', 
                              'scoreboard_score_homePeriods_1', 
                              'scoreboard_score_homePeriods_2', 
                              'scoreboard_score_homePeriods_3', 
                              'summary', 
                              'teams_away_team', 
                              'teams_home_team'])]


dfs['recordID'] = 0
counter = 0
for index, row in dfs.iterrows():
    if row['Metric'] == 'summary':
        counter += 1
        dfs.loc[index, 'recordID'] = counter

dfs['RecordID'] = (dfs['Metric'] == 'summary').cumsum()


#create the cross tab


#EXPORT TO EXCEL
dfs.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/SportsFeedAPI.xlsx', sheet_name='final', index = True)
