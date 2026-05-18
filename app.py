import os
import urllib.parse
import requests
import base64
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

import spotify
from spotify import SpotifyRecom

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Fix for getting correct https redirects behind proxies like Render/Heroku
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Use a static secret key from environment variables so sessions survive server restarts/workers
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-default-key")

# Replace these with your App's Client ID and Secret from the Spotify Developer Dashboard
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "your_client_id_here")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "your_client_secret_here")
REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI", "http://localhost:5000/callback")

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

@app.route('/login')
def login():
    scope = "user-top-read"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "show_dialog": True
    }
    auth_query = urllib.parse.urlencode(params)
    return redirect(f"{AUTH_URL}?{auth_query}")

@app.route('/callback')
def callback():
    if "error" in request.args:
        return f"Authentication failed: {request.args.get('error')}"
    
    code = request.args.get('code')
    
    # Use Basic Auth Header as recommended by Spotify OAuth 2.0 docs
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode('utf-8')
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    req_body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    
    try:
        # Add timeout so the app doesn't hang indefinitely causing the browser to stay on the Spotify Loading screen
        response = requests.post(TOKEN_URL, data=req_body, headers=headers, timeout=10)
        token_info = response.json()
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Spotify: {str(e)}"
    
    if "access_token" not in token_info:
        return f"Failed to get access token from Spotify: {token_info}"
        
    session["access_token"] = token_info.get("access_token")
    return redirect(url_for('home'))

@app.route('/')
def home():
    if "access_token" not in session:
        return render_template('home.html', logged_in=False)
    return render_template('home.html', logged_in=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/api/tracks', methods=['GET'])
def api_tracks():
    if "access_token" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    x = SpotifyRecom(session["access_token"])
    # Fetch user's top 10 played tracks
    tracks = x.get_top_tracks(10)
    return jsonify({"tracks": [str(t) for t in tracks]})

if __name__=='__main__':
    app.run(debug=True)
