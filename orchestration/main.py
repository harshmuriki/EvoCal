import mysql.connector
from flask import Flask, request, jsonify
import requests
from datetime import datetime
import time

def get_cloud_sql_connection():
    config = {
        'user': 'root',
        'password': 'aXbT|^DvTzMf%uga',
        'host': '34.69.56.41',
        'database': 'token_store',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        return cnx, cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def process_tokens():
    cnx, cursor = get_cloud_sql_connection()

    try:
        
        query = "SELECT token_string FROM token_store"
        cursor.execute(query)
        print('here')
        
        # Iterate over each token
        for (token,) in cursor:
            print(token)
            print(type(token))
            gmail_endpoint = "http://127.0.0.1:5000/email_data"
            llm_endpoint = "http://127.0.0.1:5001/process_file"
            calendar_endpoint = "http://127.0.0.1:5002/calendar_invite"

            first_response = requests.post(gmail_endpoint, json={'data': token}).json()
            print('here1')
            second_response = requests.post(llm_endpoint, json={'data': first_response}).json()
            print('here2')
            third_response = requests.post(calendar_endpoint, json={'data': token, 'body': second_response}).json()
            print('here3')
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except requests.RequestException as e:
        print(f"HTTP Request Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


    cursor.close()
    cnx.close()

if __name__ == '__main__':
    while True:

        process_tokens()
        time.sleep(3600)
        pass
