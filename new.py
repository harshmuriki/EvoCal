import base64
import json
import os
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth import impersonated_credentials
from google.oauth2 import service_account

# Path to your service account key JSON file
key_file_path = '/Users/shriyaedukulla/Desktop/Shriya/EvoCal/evocal-405516-269b9d321e17.json'

# Load the service account credentials
credentials = service_account.Credentials.from_service_account_file(
    key_file_path, scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Impersonate the service account to obtain an access token
impersonated_creds = impersonated_credentials.Credentials(
    target_principal='evocal650@gmail.com',
    source_credentials=credentials,
    lifetime=3600  # Token lifetime in seconds (adjust as needed)
)

# Get the access token
access_token = impersonated_creds.get_access_token().token

# print(f"Access Token: {access_token}")


def get_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    user_info = service.users().getProfile(userId='me').execute()
    user_email = user_info['emailAddress']
    return service, user_email

def set_gmail_watch(service, user_email, pubsub_topic):
    request = {
        'labelIds': ['INBOX'],
        'topicName': f'projects/evocal-405516/topics/{pubsub_topic}'
    }
    service.users().watch(userId='me', body=request).execute()

def process_pubsub_messages(pubsub_subscription):
    # Define the Pub/Sub subscription URL
    pubsub_url = f'https://pubsub.googleapis.com/v1/projects/YOUR_PROJECT_ID/subscriptions/{pubsub_subscription}:pull'

    while True:
        # Pull messages from Pub/Sub
        response = requests.post(pubsub_url, headers={"Authorization": access_token}, json={"maxMessages": 1})

        if response.status_code == 200:
            data = response.json()
            if 'receivedMessages' in data:
                message = data['receivedMessages'][0]
                message_data = base64.b64decode(message['message']['data']).decode('utf-8')

                # Process the message data (e.g., check for new emails)
                print(f"Received message: {message_data}")

                # Acknowledge the message
                ack_id = message['ackId']
                ack_url = f'{pubsub_url}:acknowledge'
                requests.post(ack_url, headers={"Authorization": access_token}, json={"ackIds": [ack_id]})
            else:
                print("No messages received.")
        else:
            print(f"Failed to pull messages. Status code: {response.status_code}")

if __name__ == '__main__':
    service, email = get_gmail_service()
    
    # Set the Pub/Sub topic name and subscription name
    pubsub_topic = 'projects/evocal-405516/topics/evocal'
    pubsub_subscription = 'projects/evocal-405516/subscriptions/evocal-sub'
    
    set_gmail_watch(service, email, pubsub_topic)
    process_pubsub_messages(pubsub_subscription)
