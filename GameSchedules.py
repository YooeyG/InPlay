import datetime
from datetime import date
from datetime import datetime, timedelta
import time
import pytz
import pandas as pd

# import pickle
# with open('c.pkl', 'rb') as f:
#     c = pickle.load(f)


def commence(y):
    
    df_commence = pd.DataFrame(columns=['status','Commence Time', 'Value','sport_title','home_team','away_team', 'Live Time'])
    my_list = []

    r = 0

    for x in y:
        # Parse the time string into a datetime object in the UTC time zone
        time_string = x['commence_time']    
        time = datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%SZ")
        utc_time = pytz.utc.localize(time)
        
        # Create a timezone object for New York City
        tz_nyc = pytz.timezone("America/New_York")
        
        # Convert the datetime object to New York City time
        nyc_time = utc_time.astimezone(tz_nyc)
        # Get the current date and time in New York City
        now = datetime.now(tz_nyc)

        # Format the current time and the converted time as 12-hour time strings
        now_string = now.strftime("%Y-%m-%d %I:%M %p")
        nyc_time_string = nyc_time.strftime("%Y-%m-%d %I:%M %p")


        # Compare the current time to the converted time
        if now < nyc_time:
            #print("Prematch: " + nyc_time_string, x['id']," ",x['sport_title']," ",x['home_team']," ",x['away_team'])
            s = pd.Series(["Prematch",nyc_time_string, x['id'] , x['sport_title'],x['home_team'] ,x['away_team'], now_string], index=['status', 'Commence Time','Value','sport_title','home_team','away_team','Live Time'])
            df_commence = df_commence.append(s, ignore_index=True)
        
        else:
            #print("Live Game: ",now_string ,x['id']," ",x['sport_title']," ",x['home_team']," ",x['away_team'])
            s = pd.Series(["Live Game",nyc_time_string, x['id'] , x['sport_title'],x['home_team'] ,x['away_team'], now_string], index=['status', 'Commence Time','Value','sport_title','home_team','away_team','Live Time'])
            df_commence = df_commence.append(s, ignore_index=True)

    return df_commence


# commence_df = commence(c)
# print(commence_df)
# print(type(commence_df))