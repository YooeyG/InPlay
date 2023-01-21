import requests
import pandas as pd
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup
from mappings import Team_Mapping

current_year = 2023

url = 'https://projects.fivethirtyeight.com/2023-nba-predictions/games/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


#THIS TAKES THE FULL DAY INSTANCE
section_tags = soup.find('section', class_='day')


class_names = []
texts = []
Date = []
Game = []
game = 0


section_tags = soup.find_all('section', class_='day')

for section in section_tags:
    date = section.find('h3', class_='h3').text
    #print(date)
    #print('Next Section')
    #print('')
    for table in section.find_all('table', class_='game-body'):
        #print(table)
        #print('Next Text')
        game += 1
#        print(game)
        for element in table.find_all(True):
            #print(game)
            class_name = element.get('class')
            if class_name:
                class_name = " ".join(class_name)
                class_names.append(class_name)
                texts.append(element.text)
                Date.append(date)
                Game.append(game)
df_bs4 = pd.DataFrame({'class_name': class_names, 'text': texts,
                        'date':Date, 'game': Game})

#df_bs4_game = pd.DataFrame({'date':Date, 'game': Game})


df_bs4.loc[df_bs4['class_name'].str.contains('spread'), 'marker'] = 'spread'
df_bs4.loc[df_bs4['class_name'].str.contains('number score'), 'marker'] = 'score'
df_bs4.loc[df_bs4['class_name'].str.contains('text team'), 'marker'] = 'team'
df_bs4.loc[df_bs4['class_name'].str.contains('number chance'), 'marker'] = 'probability'
df_bs4['marker'] = df_bs4['marker'].fillna('other')

#REMOVE DATA THAT IS OTHER
df_bs4 = df_bs4.query("marker != 'other'")

#print(df_bs4.head(50))


#USE 
#IDENTIFY TEAM 1 AND TEAM 2
game_count = {game: 0 for game in df_bs4['game'].unique()}

for index, row in df_bs4.iterrows():
    if row['marker'] == 'spread':
        game_count[row['game']] += 1
        df_bs4.at[index, 'spread_count'] = game_count[row['game']]

game_count = {game: 0 for game in df_bs4['game'].unique()}

for index, row in df_bs4.iterrows():
    if row['marker'] == 'team':
        game_count[row['game']] += 1
        df_bs4.at[index, 'team_count'] = game_count[row['game']]

game_count = {game: 0 for game in df_bs4['game'].unique()}

for index, row in df_bs4.iterrows():
    if row['marker'] == 'probability':
        game_count[row['game']] += 1
        df_bs4.at[index, 'probability_count'] = game_count[row['game']]

game_count = {game: 0 for game in df_bs4['game'].unique()}

for index, row in df_bs4.iterrows():
    if row['marker'] == 'score':
        game_count[row['game']] += 1
        df_bs4.at[index, 'score_count'] = game_count[row['game']]

#CONCATENATE NAMES
#Initialize Metric_Name column with empty string
df_bs4['Metric_Name'] = ""

# Check if spread_count is not NaN and if so, create new Metric_Name by concatenating marker and spread_count
df_bs4.loc[~df_bs4['spread_count'].isna(), 'Metric_Name'] = df_bs4['marker'] + '_' + df_bs4['spread_count'].astype(str)

# Check if game_count is not NaN and if so, create new Metric_Name by concatenating marker and game_count
df_bs4.loc[~df_bs4['team_count'].isna(), 'Metric_Name'] = df_bs4['marker'] + '_' +  df_bs4['team_count'].astype(str)

# Check if probability_count is not NaN and if so, create new Metric_Name by concatenating marker and probability_count
df_bs4.loc[~df_bs4['probability_count'].isna(), 'Metric_Name'] = df_bs4['marker'] + '_' +  df_bs4['probability_count'].astype(str)

# Check if score_count is not NaN and if so, create new Metric_Name by concatenating marker and score_count
df_bs4.loc[~df_bs4['score_count'].isna(), 'Metric_Name'] = df_bs4['marker'] + '_' +  df_bs4['score_count'].astype(str)

#KEEP COLUMNS
df_bs4 = df_bs4[['date','game','Metric_Name','text']]
cross_tab = pd.crosstab(index=df_bs4['game'], columns=df_bs4['Metric_Name'], values=df_bs4['text'], aggfunc='first')
df_Date = df_bs4[['game','date']].drop_duplicates(subset=['game','date'])

#MERGE
cross_tab = pd.merge(df_Date, cross_tab, on='game')

#FIX THE DATE FORMAt
cross_tab['date'] = cross_tab['date'].apply(lambda x: datetime.strptime(x + ', ' + str(datetime.now().year), '%A, %b. %d, %Y'))


#FILL IN THE SPREADS
cross_tab['spread_1.0'] = pd.to_numeric(cross_tab['spread_1.0'], errors='coerce')
cross_tab['spread_2.0'] = pd.to_numeric(cross_tab['spread_2.0'], errors='coerce')

print(cross_tab['spread_1.0'].dtype)
print(cross_tab['spread_2.0'].dtype)

cross_tab['spread_1'] = cross_tab['spread_1.0'].where(~cross_tab['spread_1.0'].isna(), cross_tab['spread_2.0'] * -1)
cross_tab['spread_2'] = cross_tab['spread_2.0'].where(~cross_tab['spread_2.0'].isna(), cross_tab['spread_1.0'] * -1)

#print(cross_tab.head(50))


cross_tab = cross_tab[['game','date','probability_1.0','probability_2.0','score_1.0', 'score_2.0','team_1.0','team_2.0','spread_1','spread_2']]

# rename all columns
new_col_names = ['game','date','prob_1','prob_2','score_1', 'score_2','team_1','team_2','spread_1','spread_2']
cross_tab.columns = new_col_names


#Team merge name
cross_tab = pd.merge(cross_tab, Team_Mapping, left_on='team_1', right_on='Team Name', how='inner')
cross_tab = cross_tab[['game','date','prob_1','prob_2','score_1', 'score_2','team_1','team_2','spread_1','spread_2','Team']]
new_col_names = ['game','date','prob_1','prob_2','score_1', 'score_2','team_1','team_2','spread_1','spread_2','Team_1']
cross_tab.columns = new_col_names


cross_tab = pd.merge(cross_tab, Team_Mapping, left_on='team_2', right_on='Team Name', how='inner')
cross_tab = cross_tab[['game','date','prob_1','prob_2','score_1', 'score_2','spread_1','spread_2','Team_1','Team']]

print(cross_tab.shape)
new_col_names2 =  ['Game','Date','Prob_1','Prob_2','Score_1', 'Score_2','Spread_1','Spread_2','Team_1','Team_2']
cross_tab.columns = new_col_names2


#TODAY FLAG

#CROSS TAB
#print(df_bs4.head(50))
#print(cross_tab.head(50))


cross_tab.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/"bs4538.xlsx', sheet_name='final', index = True)


