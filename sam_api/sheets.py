import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
import sam_api as sam_api
import pandas as pd
import numpy as np
import cleaner
import readable
import getopt, sys


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1aesRU_T-oOfRMUxC2c6zwe9QRYXwAgo9-izYE_dPapI"


def setup():
    creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            
    service = build("sheets", "v4", credentials=creds)
    return service

def update_cells(df):
    values = [df.columns.values.tolist()]
    values.extend(df.values.tolist())

    return values

def add_sheet_request(requests, date):
    # add sheet for today
    requests.append(
        {
            "addSheet":{
                "properties": {"title": date}
            }
        }
    )
    return requests


      
def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dys:e:", ["date=", "yesterday", "start=", "end="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
        
    yesterday = False
    
    for option, arg in opts:
        match option:
            case "-y":
                yesterday = True
            case "--yesterday":
                yesterday = True
                
    if yesterday:
        yes = datetime.date.today() - datetime.timedelta(days=1)
        date = yes.strftime("%m/%d/%Y")
    else:
        date = datetime.date.today().strftime("%m/%d/%Y")
    
    DEBUG = False
    
    service = setup()
    batch_requests = []
    add_sheet_request(batch_requests, date)
    
    body = {"requests": batch_requests}
    try:
        batch_response = (
            service.spreadsheets()
            .batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body)
            .execute()
        )
    except Exception:
        print("Updating sheet instead.")
    
    raw_df = sam_api.main(date, date)
    readable_df = readable.readable(raw_df)
    values = update_cells(readable_df)
    
    body = {"values": values}
    if DEBUG:
        print(body)
    value_response = (
        service.spreadsheets().values()
        .update(spreadsheetId=SPREADSHEET_ID,
                range=f"'{date}'!A:Z",
                body=body,
                valueInputOption="USER_ENTERED")
        .execute()
    )
    
    


if __name__ == "__main__":
    main()