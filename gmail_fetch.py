import base64
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def get_gmail_service():
    # ... [Your existing authentication code] ...
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
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    messages = results.get('messages', [])
    email_data = []

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        payload = msg['payload']
        headers = payload.get('headers')

        email_info = {
            'subject': next((header['value'] for header in headers if header['name'] == 'Subject'), None),
            'from': next((header['value'] for header in headers if header['name'] == 'From'), None),
            'date': next((header['value'] for header in headers if header['name'] == 'Date'), None),
            'body': ''
        }

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    decoded_data = base64.urlsafe_b64decode(data.encode('ASCII'))
                    email_info['body'] = decoded_data.decode('utf-8')
                    break
        else:
            data = payload['body']['data']
            decoded_data = base64.urlsafe_b64decode(data.encode('ASCII'))
            email_info['body'] = decoded_data.decode('utf-8')

        email_data.append(email_info)

    with open(f'email_data_{user_email.split("@")[0]}.json', 'w') as f:
        json.dump(email_data, f, indent=4)

if __name__ == '__main__':
    service, email = get_gmail_service()
    get_unread_emails(service, email)
