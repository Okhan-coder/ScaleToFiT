import requests
from flask import Flask, redirect, request, session, url_for

# ClientID:2162ca2b62e9e6ccca609f880e75f2073782f5bb56b72bc462a68d6bff044560
# Secret:2df84d48abfb3ed4b224f3efe56edbd881d085bcb5e750a42a500c6b6329ec77

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return 'Welcome to the Withings Flask API!'

@app.route('/authorize')
def authorize():
    # Redirect to Withings authorization URL
    return redirect(
        f"https://account.withings.com/oauth2_user/authorize2?response_type=code&client_id=2162ca2b62e9e6ccca609f880e75f2073782f5bb56b72bc462a68d6bff044560&state=YOUR_RANDOM_STRING&scope=user.info,user.metrics,user.activity&https://sweet-tuna-safe.ngrok-free.app//oauth2callback"
    )

@app.route('/oauth2callback')
def oauth2callback():
    auth_code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'client_id': '2162ca2b62e9e6ccca609f880e75f2073782f5bb56b72bc462a68d6bff044560',
        'client_secret': '2df84d48abfb3ed4b224f3efe56edbd881d085bcb5e750a42a500c6b6329ec77',
        'code': 'auth_code',
        'redirect_uri': 'https://sweet-tuna-safe.ngrok-free.app/oauth2callback'
    }
    # Exchange the authorization code for an access token
    r = requests.post('https://wbsapi.withings.net/v2/oauth2', data=data)
    access_token = r.json()['body']['access_token']
    session['access_token'] = access_token
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)