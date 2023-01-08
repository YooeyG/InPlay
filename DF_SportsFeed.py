import pandas as pd
from SportsFeed_API import process_metric_name

def DF_SportsFeed_Prep(df):
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
    print(dfz.dtypes)

    dfz[['scoreboard_score_away', 'scoreboard_score_home']] = dfz[['scoreboard_score_away', 'scoreboard_score_home']].apply(pd.to_numeric)
    dfz = dfz[['lastUpdated','scoreboard_currentPeriod','scoreboard_periodTimeRemaining','teams_home_team', 'scoreboard_score_home', 'teams_away_team','scoreboard_score_away']]

    return dfz