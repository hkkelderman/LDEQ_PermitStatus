#importing libraries
import requests
from csv import reader
from bs4 import BeautifulSoup
import pandas as pd
import win32com.client as win32
from functions import get_payload, get_status, send_updates, differencing

#scraping new data from LDEQ website
payload = get_payload()
df = get_status(payload)
df.to_csv('temp_file.csv',index=False)

#importing data
old = pd.read_csv('old_file.csv') #old version of database
new = pd.read_csv('temp_file.csv') #recently scraped version of database
AIs = pd.read_csv('LA_AIs.csv').AI_Num.to_list() #list of AIs of concern

#finding rows of data with changes made or new rows of data added for AIs of concern
updates = differencing(old,new,AIs)
updates.to_csv('DataUpdates.csv',index=False)

#email new additions to Sasha
length = len(updates)
send_updates(length)

#once new additions sent to Sasha, write new scrape of data as "old_file.csv"
new.to_csv('old_file.csv',index=False)