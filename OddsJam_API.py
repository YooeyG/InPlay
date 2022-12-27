#import Settings as s
#import sys
#print(sys.path)

#from Settings import api_key, API_KEY, SPORT, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT, requests

#print("This is Odds Jam")
#print("Global Variables:", *globals(),sep='\n')    


def JAM_API():
    odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?', params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
        })

    a = []
    if odds_response.status_code != 200:
        print('nope')
    else:
        odds_json = odds_response.json()
        a.append(odds_json)

        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])

    b = a[0]
    return b


#print("Global Variables:", *globals(),sep='\n')    
