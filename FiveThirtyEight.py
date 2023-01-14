import requests
import pandas as pd
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup

current_year = 2023


teams = ["Wizards", "Trail Blazers", "Suns", "Spurs", "Lakers",
        "Raptors", "Pelicans", "Nuggets", "Nets", "Mavericks", 
        "Magic", "Knicks", "Kings", "Hornets", "Heat", "Grizzlies", 
        "Celtics", "Cavaliers", "Bucks", "76ers", "Warriors", 
        "Timberwolves", "Thunder", "Rockets", "Pistons", "Pacers", 
        "Jazz", "Hawks", "Clippers", "Bulls"]


url = 'https://projects.fivethirtyeight.com/2023-nba-predictions/games/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


z = 0
table_tags = soup.find_all('table', class_='game-body')
for table in table_tags:
    td_tags = table.find_all('td')
    for td in td_tags:
        z += 1
#        print(td.text, z)

#print(type(td_tags))

data = [td.text for td in td_tags]
df = pd.DataFrame(data, columns=["Text"])


section_tags = soup.find_all('section', class_='day')
df = pd.DataFrame(columns=["Text"])

# extract the text for each section tag and add it to a new row in the DataFrame
for section in section_tags:
    for text in section.stripped_strings:
        df = df.append({'Text': text}, ignore_index=True)

df['marker'] = np.where(df['Text'].isin(teams), 1, 0)
df['marker'] = np.where(df['Text'].str.contains('%'), 1, df['marker'])
df['marker'] = np.where(df['Text'].str.contains('-'), 1, df['marker'])
df['marker_date'] = np.where(df['Text'].str.contains('Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday'), 1, 0)

#Alternative Date Detection
#df['marker_date'] = np.where(df['Text'].str.contains('[A-Za-z]{3,9}, [A-Za-z]{3}.[ 0-9]{1,2}', case=False), 1, 0)

df['Keep'] = df['marker_date'] + df['marker']
df = df[df['Keep'] != 0]


#PATTERN RECOGNITION
df['Game ID'] = 0
df['Date Group'] = None

game_id = 0
date_group = None

for index, row in df.iterrows():
    if row['marker_date'] == 1:
        game_id = 0
        date_group = row['Text']
    elif row['marker'] == 1:
        if game_id % 5 == 0:
            game_id = 1
        else:
            game_id += 1

    df.at[index, 'Game ID'] = game_id
    df.at[index, 'Date Group'] = date_group

df = df[df['Game ID'] != 0]


#NOW CLUSTER THE GROUPS
df['Group'] = 0
group_counter = 0
for index, row in df.iterrows():
    if row['Game ID'] == 1:
        group_counter += 1
    df.at[index, 'Group'] = group_counter


#IDENTIFY TEAM 1 AND TEAM 2
team_count = {group: 0 for group in df['Group'].unique()}
for index, row in df.iterrows():
    if row['Text'] in teams:
        team_count[row['Group']] += 1
        df.at[index, 'team_count'] = team_count[row['Group']]

#PROBABILITY ID FOR EACH GROUP
df['Prob Num'] = None
for group in df['Group'].unique():
    prob_count = 0
    for index, row in df[df['Group']==group].iterrows():
        if '%' in row['Text']:
            prob_count +=1
            df.at[index, 'Prob Num'] = prob_count

df['Index'] = np.where(df['team_count'] == 1.0, 'Team 1',
                        np.where(df['team_count'] == 2.0, 'Team 2',
                        np.where(df['Text'].str.contains('-', na=False), 'Spread',
                        np.where(df['Prob Num'] == 1, 'Probability 1', 'Probability 2'))))

df['ID'] = df.apply(lambda x: x['Date Group'] + ' - ' + str(x['Group']), axis=1)


#CREATE THE CROSS TAB
cross_tab = pd.crosstab(index=df['ID'], columns=df['Index'], values=df['Text'], aggfunc='first')
cross_tab.reset_index(inplace=True)


#print(cross_tab.columns)
#print(type(cross_tab))

#SPLIT ID
cross_tab[['Date Group', 'Game ID']] = cross_tab['ID'].str.split(' - ', expand=True)
cross_tab['Date Final'] = cross_tab['Date Group'].apply(lambda x: datetime.strptime(x + ' ' + str(current_year), '%A, %b. %d %Y').strftime("%B %d, %Y"))

now = datetime.now()
cross_tab['Today ID'] = cross_tab['Date Final'].apply(lambda x: 'Today' if datetime.strptime(x, '%B %d, %Y').date() == now.date() else 'Not Today')

print(cross_tab.columns)

cross_tab = cross_tab.drop(columns=['ID', 'Date Group'], axis=1)

print(cross_tab.head(25))
print(cross_tab.columns)

print(cross_tab.index.name)
#cross_tab.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/"extracted_text.xlsx', sheet_name='final', index = True)





