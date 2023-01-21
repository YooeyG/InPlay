'FROM MODULE IMPORTS'
from __future__ import print_function
from datetime import date
from datetime import datetime

from dotenv import load_dotenv    

import sys
import json
import requests
import time
import sys
import os

# The sys.prefix attribute returns the installation prefix of the current Python environment
virtual_environment_path = sys.prefix
virtual_environment_name = os.path.basename(virtual_environment_path)
print("Environment location:", virtual_environment_name)
print("")

#Environment Variables
load_dotenv()

'ODDS JAM API SETTINGS'
API_KEY = os.getenv('api_key')
SPORT = 'NBA' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across allsports
REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited
ODDS_FORMAT = 'american' # decimal | american
DATE_FORMAT = 'iso' # iso | unix


'SPORTSFEED API SETTINGS'
STATUS = 'scheduled' #scheduled, in progress, final, canceled, delayed
LEAGUE = 'NBA' #League Options NFL, NBA, MLB, NHL, NCAAF, or NCAAB

#DATE
today = datetime.now()
today_string = today.strftime("%Y-%m-%d")
print("Today's Date:", today_string)






print("Python Location:", sys.executable)
print("")
#print(sys.prefix)


'IMPORT MODULE LOGIC'
file_path = requests.__file__  #use requests module to test the path
dir = os.path.dirname(file_path)
json_module = sys.modules['json']
json_module_path = os.path.abspath(json_module.__file__)


print("Current Script File Path: ",__file__)
print("")
#print("Packages Modules File Path", json_module_path)
print("")
print(f"Import path: {dir}")
print("")
print("Environmental Search Paths:", *sys.path,sep='\n')    
print("")
print('API',API_KEY)

'GLOBALS VARIABLE PRINTOUTS'
#print()
#print("Global Variables:", *globals(),sep='\n')    




# Set the path to the directory you want to list
# directory_path = '/Users/anaconda3/lib/python3.8/site-packages/'
# # Use the listdir() function to get a list of the files in the directory
# files = os.listdir(directory_path)
# # Print the list of files
# print(files)
