import datetime
from datetime import date
from datetime import datetime, timedelta
import time
import pytz

  
def commence(y):

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
            #print("Prematch: current time is " + now_string + " and game time is " + nyc_time_string)
            GameTime = 'Pregame: Start Time' + nyc_time_string
        else:
            #print("Live game: current time is " + now_string + " and game time is " + nyc_time_string)
            GameTime = 'Live'
        #place into a dataframe for merging


for x in odds_json:
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
        print("Prematch: " + nyc_time_string, x['id']," ",x['sport_title']," ",x['home_team']," ",x['away_team'])
    else:
        print("Live Game: ",now_string ,x['id']," ",x['sport_title']," ",x['home_team']," ",x['away_team'])
