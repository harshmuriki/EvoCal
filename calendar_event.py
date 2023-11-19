from google.oauth2 import credentials
import googleapiclient.discovery
from datetime import datetime, timedelta
import os
from google_auth_oauthlib.flow import InstalledAppFlow  # Add this import
import json

def get_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    if os.path.exists('calendar_token.json'):
        creds = credentials.Credentials.from_authorized_user_file('calendar_token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(googleapiclient.discovery.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        with open('calendar_token.json', 'w') as token:
            token.write(creds.to_json())

    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    return service

def create_calendar_event(service, event_data):
    # Define event details
    # print(event_data)
    for event_ in event_data:
        # print(event_)
        event = {
            'summary': event_['name'],
            'location': event_['location'],
            'start': {
                'dateTime': event_['start_time'],
                'timeZone': 'EST',
            },
            'end': {
                'dateTime': event_['end_time'],
                'timeZone': 'EST',
            },
        }

        # Insert the event into the calendar
        event = service.events().insert(calendarId='primary', body=event).execute()

        # print(f'Event created: {event["htmlLink"]}')

if __name__ == '__main__':
    calendar_service = get_calendar_service()
    with open('event_data.json', 'r') as file:
        event_data = json.load(file)
    create_calendar_event(calendar_service, event_data)
