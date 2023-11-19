# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
import base64
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()


def get_gmail_service(REFRESH_TOKEN):
    # Create a credentials object using the provided information
    creds = Credentials(
        None,
        client_id=os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        refresh_token=REFRESH_TOKEN,
        token_uri='https://oauth2.googleapis.com/token'
    )

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_unread_emails(service):
    one_hour_ago = datetime.now() - timedelta(hours=1)
    query_timestamp = int(time.mktime(one_hour_ago.timetuple()))
    query = f'is:unread after:{query_timestamp}'

    results = service.users().messages().list(
        userId='me', labelIds=['INBOX'], q=query).execute()
    messages = results.get('messages', [])
    data = ""

    for message in messages:
        msg = service.users().messages().get(
            userId='me', id=message['id'], format='full').execute()
        payload = msg['payload']

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    decoded_data = base64.urlsafe_b64decode(
                        data.encode('ASCII'))
                    data += decoded_data.decode('utf-8')
                    break
        else:
            data = payload['body']['data']
            decoded_data = base64.urlsafe_b64decode(data.encode('ASCII'))
            data += decoded_data.decode('utf-8')

        data += "!@#$%^&*()" + "\n\n"

        return data


if __name__ == '__main__':
    service = get_gmail_service(
        'ya29.a0AfB_byBQynIdUUf38J-51xiTAbeKOD5_mIXg2fJWkGjAYJnl2JhrShkre1wI9kN2KB_ng9w4DNW15p_W3_YkgVx0o3kNMNLSCCFBUd22MrCMel3bTr84jZfJ__LpYLcJUjBpjcOO_9ZMS_4hfLZWnA6IXbhKm1S-SqvJaCgYKAVcSARESFQHGX2MiO-PNusGpZKAjrK4ifcGOsQ0171')
    get_unread_emails(service)
