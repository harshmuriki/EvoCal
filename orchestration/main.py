import mysql.connector
from flask import Flask, request, jsonify
import requests

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
        # Query to get all tokens
        query = "SELECT token_string FROM token_store"
        cursor.execute(query)

        # Iterate over each token
        for (token,) in cursor:
            first_url = "https://gmailpackage-3l6j2umkza-uc.a.run.app"
            second_url = "https://messageparsing-3l6j2umkza-uc.a.run.app"

            # First API call
            first_response = requests.post(first_url, json={'data': token}).json()

            # Second API call with the response of the first
            second_response = requests.post(second_url, json={'data': first_response}).json()
            pass
    except mysql.connector.Error as err:
        print(f"Error: {err}")