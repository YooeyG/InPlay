'FROM MODULE IMPORTS'
from __future__ import print_function
from datetime import date
from datetime import datetime

import json
import requests
import time
import sys
import os

'META DATA'
api_key = 'e6a9e9cfd798098ed200b73cb0201f60'

API_KEY = api_key
SPORT = 'NBA' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports
REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited
ODDS_FORMAT = 'american' # decimal | american
DATE_FORMAT = 'iso' # iso | unix



'IMPORT MODULE LOGIC'
file_path = requests.__file__ #use requests module to test the path
dir = os.path.dirname(file_path)
print("Current File Path: ",__file__)
print("")
print(f"Import path: {dir}")
print("")
print("Environmental Search Paths:", *sys.path,sep='\n')    

'GLOBALS'
print()
#print("Global Variables:", *globals(),sep='\n')    

#Big Picture Loan with Brian H and Amy Bane due 12/19
#Petsense with Mike Stern 
#KEH