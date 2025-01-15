import requests
import json
from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
import pickle 
import os.path 
import base64 
import email 
from bs4 import BeautifulSoup 

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getStockData(symbol):

    
    key = open('Keys\\Key.txt', 'r').read()
    
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + symbol + '&apikey=' + key

    r = requests.get(url)
    data = r.json()
    
    return data

def getDailyTimeSeries(symbol):
    
    key = open('Keys\\Key.txt', 'r').read()
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=' + key

    r = requests.get(url)
    data = r.json()

    return data

def getIntraDayTimeSeries(symbol):

    key = open('Keys\\Key.txt', 'r').read()
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + symbol + '&interval=5min&apikey=' + key

    r = requests.get(url)
    data = r.json()

    return data

def getGmailData():
    creds = None

    if os.path.exists('Keys\\token.pickle'):
        with open('Keys\\token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('Keys\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('Keys\\token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    result = service.users().messages().list(maxResults=10, userId='me').execute()

    msgs = result.get('messages')

    emails = []

    for msg in msgs:
        s = service.users().messages().get(userId='me', id=msg['id']).execute()

        try:
            payload = s['payload']
            part = payload['parts'][0]
            headers = payload['headers']

            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                if header['name'] == 'From':
                    sender = header['value']
                if header['name'] == 'Date':
                    date = header['value']
                    
            data = part['body']['data']
            data = data.replace('-','+').replace('_','/')
            decodedData = base64.b64decode(data)
            soup = BeautifulSoup(decodedData, 'lxml')
            body = soup.get_text()

            emails.append([str(sender), str(subject), str(date), body])
            
        except:
            pass
    
    return emails



