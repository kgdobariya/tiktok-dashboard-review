# You will need to install Flask first: pip install Flask requests
from flask import Flask, request, redirect, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- IMPORTANT: Do NOT put your real keys here in the public repo. ---
# --- You will add them locally on your computer in Step 4. ---
TIKTOK_CLIENT_KEY = "PASTE_YOUR_CLIENT_KEY_HERE_ON_YOUR_COMPUTER_ONLY"
TIKTOK_CLIENT_SECRET = "PASTE_YOUR_CLIENT_SECRET_HERE_ON_YOUR_COMPUTER_ONLY"

REDIRECT_URI = "http://127.0.0.1:5000/callback"

@app.route('/')
def homepage():
    login_url = (f"https://www.tiktok.com/v2/auth/authorize?"
                 f"client_key={TIKTOK_CLIENT_KEY}&"
                 f"scope=user.info.basic,video.list&"
                 f"response_type=code&"
                 f"redirect_uri={REDIRECT_URI}&"
                 f"state=12345")
    return f'<h1>Demo for TikTok App Review</h1><p>This page demonstrates the start of the authentication flow.</p><a href="{login_url}">Login with TikTok</a>'

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    token_payload = {
        "client_key": TIKTOK_CLIENT_KEY,
        "client_secret": TIKTOK_CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }
    r = requests.post(token_url, data=token_payload)
    access_token = r.json().get("access_token")
    session['access_token'] = access_token
    return redirect('/userinfo')

@app.route('/userinfo')
def get_user_info():
    access_token = session.get('access_token')
    if not access_token: return redirect('/')
    user_info_url = "https://open.tiktokapis.com/v2/user/info/?fields=open_id,username,display_name,avatar_url"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(user_info_url, headers=headers)
    user_data = r.json()
    display_name = user_data.get("data", {}).get("user", {}).get("display_name", "N/A")
    avatar_url = user_data.get("data", {}).get("user", {}).get("avatar_url", "")
    return f"""
        <h1>TikTok Login Successful!</h1>
        <h2>Welcome, {display_name}</h2>
        <img src="{avatar_url}" width="100">
        <p>This demonstrates the complete and successful authentication flow for our app review.</p>
    """

if __name__ == '__main__':
    app.run(port=5000)
