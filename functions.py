import requests
from csv import reader
from bs4 import BeautifulSoup
import pandas as pd
import win32com.client as win32

#function for retrieving payload values
def get_payload(url='https://internet.deq.louisiana.gov/portal/ONLINESERVICES/CHECK-PERMIT-STATUS'):
    """Using the base url for the permit status website, this function retrieves the necessary headers required for a POST
    request that returns the entire permit status database. 
    
    Params:
    url - 'https://internet.deq.louisiana.gov/portal/ONLINESERVICES/CHECK-PERMIT-STATUS'
    
    Returns a dictionary used as the payload for the POST request."""
    
    #form values that don't change
    payload = {"__EVENTTARGET": "dnn$ctr489$dnn",
          "__EVENTARGUMENT": "CSV,Export,,M"}
    
    #form values to be retrieved from get request
    headers = ["__VIEWSTATE","__VIEWSTATEGENERATOR","__VIEWSTATEENCRYPTED","__EVENTVALIDATION",]
    
    #performing request
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    for head in headers:
        val = soup.find(id=head)['value']
        payload[head] = val
        
    return payload

#function for retrieving permit status data
def get_status(payload, url='https://internet.deq.louisiana.gov/portal/ONLINESERVICES/CHECK-PERMIT-STATUS'):
    """Takes the payload from the GET request and attaches it to the POST request, which retrieves the most recent, full
    dataset from the website. 
    
    Params:
    payload - dictionary of form variable/value pairs that are used to retrieve the data
    url - 'https://internet.deq.louisiana.gov/portal/ONLINESERVICES/CHECK-PERMIT-STATUS'
    
    Currently returns a dataframe."""
    
    #performing POST request
    q = requests.post('https://internet.deq.louisiana.gov/portal/ONLINESERVICES/CHECK-PERMIT-STATUS', data=payload)
        
    #splitting text into rows
    text = q.text.splitlines()
    rows = []

    for line in reader(text, skipinitialspace=True):
        rows.append(line)
    
    data = rows[1:]
    columns = rows[0]
    df = pd.DataFrame(data,columns=columns)
    df.MASTER_AI_ID = pd.to_numeric(df.MASTER_AI_ID)
    df.RECEIVED_DATE = pd.to_datetime(df.RECEIVED_DATE)
    df.STATUS_DATE = pd.to_datetime(df.STATUS_DATE)
    df.EFFECTIVE_START_DATE = pd.to_datetime(df.EFFECTIVE_START_DATE)
    df.EXPIRATION_DATE = pd.to_datetime(df.EXPIRATION_DATE)
    
    return df

#function for differencing the old and new data
def differencing(old,new,AIs):
    """Takes the old data download and the new data download, standardizes their datatypes, and then returns a dataframe
    containing the newest additions/changes made to the dataset. It also filters for the AIs we care about.
    
    Params:
    old - dataframe of old version of the database
    new - dataframe of newly scraped version of the database
    AIs - list of AIs we want to track
    
    Currently returns a dataframe."""
    
    for df in [old, new]:
        df.RECEIVED_DATE = pd.to_datetime(df.RECEIVED_DATE)
        df.STATUS_DATE = pd.to_datetime(df.STATUS_DATE)
        df.EFFECTIVE_START_DATE = pd.to_datetime(df.EFFECTIVE_START_DATE)
        df.EXPIRATION_DATE = pd.to_datetime(df.EXPIRATION_DATE)
        
    updates = pd.concat([new,old,old]).drop_duplicates(keep=False) #all updates
    filtered = updates[updates.MASTER_AI_ID.isin(AIs)] #filtered updates
    
    return filtered

#function for sending data updates to Sasha
def send_updates(length):
    """Takes the CSV with updates from the permit status website and sends them to Sasha. 
    
    Params:
    length - the number of permit status updates
    
    Currently returns a dataframe."""
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'kkelderman@environmentalintegrity.org'
    mail.Subject = 'LDEQ Permit Status Updates'
    mail.Body = 'This is an automated message. Attached is a CSV with {} updates to permits.'.format(length)

    attachment  = "C:/Users/kkelderman/Documents/00_Coding Projects/O&G/LA EDMS Alert/Alert/DataUpdates.csv"
    mail.Attachments.Add(attachment)

    mail.Send()