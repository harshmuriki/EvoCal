from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import base64
import time
from datetime import datetime, timedelta

def get_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    if os.path.exists(f'token.json'):
        creds = Credentials.from_authorized_user_file(f'token.json', SCOPES)
    #TODO: Add a check to see if the token is expired
    #TODO: User needs an option to select a different email account if needed 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        with open(f'token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    user_info = service.users().getProfile(userId='me').execute()
    user_email = user_info['emailAddress']
    return service, user_email

def get_unread_emails(service, user_email):
    one_hour_ago = datetime.now() - timedelta(hours=1)
    query_timestamp = int(time.mktime(one_hour_ago.timetuple()))
    query = f'is:unread after:{query_timestamp}'

    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=query).execute()
    messages = results.get('messages', [])
    f = open(f'email_{user_email.split("@")[0]}.txt', 'w')

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        payload = msg['payload']

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    decoded_data = base64.urlsafe_b64decode(data.encode('ASCII'))
                    f.write(decoded_data.decode('utf-8'))
                    break
        else:
            data = payload['body']['data']
            decoded_data = base64.urlsafe_b64decode(data.encode('ASCII'))
            f.write(decoded_data.decode('utf-8'))
        
        f.write("!@#$%^&*()" + "\n\n")
    f.close()

if __name__ == '__main__':
    service, email = get_gmail_service()
    get_unread_emails(service, email)