from google.oauth2.credentials import Credentials
import googleapiclient.discovery
import os
from flask import Flask, request, jsonify


def get_calendar_service(REFRESH_TOKEN):
    creds = Credentials(
        None,
        client_id=os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        refresh_token=REFRESH_TOKEN,
        token_uri='https://oauth2.googleapis.com/token'
    )

    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=creds)
    return service


def create_calendar_event(service, event_data):

    for email in event_data:
        for event_ in email:
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
            event = service.events().insert(calendarId='primary', body=event).execute()


app = Flask(__name__)


@app.route('/calendar_invite', methods=['POST'])
def calendar_data():
    try:
        token = request.json['data']
        data = request.json['body']
        assert isinstance(token, str)
        service = get_calendar_service(token)
        create_calendar_event(service, event_data=data)
        return jsonify({"True"})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
    pass
