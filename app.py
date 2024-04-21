import time
from urllib.parse import urlencode

import requests
from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['CLIENT_ID'] = '2162ca2b62e9e6ccca609f880e75f2073782f5bb56b72bc462a68d6bff044560'
app.config['CLIENT_SECRET'] = '2df84d48abfb3ed4b224f3efe56edbd881d085bcb5e750a42a500c6b6329ec77'
app.config['REDIRECT_URI'] = 'https://sweet-tuna-safe.ngrok-free.app'

AUTHORIZE_URL = 'https://account.withings.com/oauth2_user/authorize2'
TOKEN_URL = 'https://wbsapi.withings.net/v2/oauth2'
DATA_URL = 'https://wbsapi.withings.net/v2/measure'

@app.route('/')
def index():
    return 'Welcome to the Withings Flask API!'

@app.route('/authorize')
def authorize():
    # Redirect to Withings authorization URL
    params = {
        'response_type': 'code',
        'client_id': app.config['CLIENT_ID'],
        'state': 'your_random_state_string',
        'scope': 'user.metrics',
        'redirect_uri': app.config['REDIRECT_URI'],
        # Add the generated signature here
    }
    authorize_url = f"{AUTHORIZE_URL}?{urlencode(params)}"
    return redirect(authorize_url)

@app.route('/oauth2callback')
def oauth2callback():
    auth_code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'client_id': app.config['CLIENT_ID'],
        'client_secret': app.config['CLIENT_SECRET'],
        'code': auth_code,
        'redirect_uri': app.config['REDIRECT_URI'],
    }

    # Exchange the authorization code for an access token
    response = requests.post(TOKEN_URL, data=data)
    token_data = response.json()

    if response.status_code == 200 and 'body' in token_data and 'access_token' in token_data['body']:
        access_token = token_data['body']['access_token']
        refresh_token = token_data['body']['refresh_token']
        user_id = token_data['body']['userid']

        session['access_token'] = access_token
        session['refresh_token'] = refresh_token
        session['user_id'] = user_id

        # Fetch data using the access token
        headers = {'Authorization': f"Bearer {access_token}"}
        params = {
            'action': 'getmeas',
            'userid': user_id,
            'meastype': 4,  # 4 for weight
            'lastupdate': int(time.time() - 24 * 60 * 60),  # 24 hours ago
        }

        response = requests.get(DATA_URL, headers=headers, params=params)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        data = response.json()

        if 'body' in data and 'measuregrps' in data['body']:
            measurements = data['body']['measuregrps'][0]['measures']
            for measurement in measurements:
                weight = measurement['value']
                print(f"Weight: {weight} kg")

        return redirect(url_for('index'))
    else:
        return "Error: Failed to obtain access token", 500

if __name__ == '__main__':
    app.run(debug=True)
