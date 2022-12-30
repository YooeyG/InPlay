# Import the necessary objects, functions, and variables from the settings module
from Settings import API_KEY, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT, requests

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

