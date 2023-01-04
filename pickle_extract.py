import pandas as pd
import requests
import time

# Set the URL for the API endpoint
url = "http://api.example.com/endpoint"

# Set the interval for making API calls (in seconds)
interval = 60

# Create an empty dataframe to store the data
df = pd.DataFrame()

# Set a flag variable to control the loop
flag = True

while flag:
    # Make the API call
    response = requests.get(url)

    # Check the status code of the response
    if response.status_code == 200:
        # If the call is successful, get the data from the response
        data = response.json()

        # Update the dataframe with the new data
        df = df.append(data, ignore_index=True)

        # Plot the updated data
        df.plot()
    else:
        # If the call is not successful, print an error message
        print("API call failed with status code {}".format(response.status_code))

    # Sleep for the specified interval before making the next API call
    time.sleep(interval)

    # Check if the user wants to stop the data pull
    user_input = input("Enter 'stop' to stop the data pull: ")
    if user_input.lower() == 'stop':
        flag = False



#with open('df_livefeed.pkl', 'rb') as infile:
#    c = pickle.load(infile)




#EXPORT TO EXCEL
#c.to_excel(r'~/Desktop/Coding/Python Scripts/Sports Betting/OddsJamLiveAPI.xlsx', sheet_name='final', index = True)
