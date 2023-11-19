import mysql.connector
from datetime import datetime
from flask import Flask, request, jsonify

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

def add_token_if_not_exists(token):
    cnx, cursor = get_cloud_sql_connection()
    returnval = False
    # Check if the token already exists
    check_query = "SELECT COUNT(*) FROM token_store WHERE token_string = %s"
    cursor.execute(check_query, (token,))
    (count,) = cursor.fetchone()

    if count == 0:
        # Token doesn't exist, add it
        insert_query = "INSERT INTO token_store (token_string, last_seen) VALUES (%s, %s)"
        current_time = datetime.now()
        cursor.execute(insert_query, (token, current_time))
        cnx.commit()
        returnval = True
    else:
        print("Token already exists.")

    cursor.close()
    cnx.close()
    return returnval

app = Flask(__name__)
@app.route('/upload_token', methods=['POST'])
def upload_token():
    try:
        token = request.json['data']
        assert isinstance(token, str)
        result = add_token_if_not_exists(token)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
    pass