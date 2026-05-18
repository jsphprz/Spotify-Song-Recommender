import os
import urllib.parse
import requests
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from dotenv import load_dotenv
import spotify
from spotify import SpotifyRecom

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

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
    req_body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    response = requests.post(TOKEN_URL, data=req_body)
    token_info = response.json()
    
    if "access_token" not in token_info:
        return f"Failed to get access token from Spotify: {token_info}"
        
    session["access_token"] = token_info.get("access_token")
    return redirect(url_for('home'))

@app.route('/')
def home():
    if "access_token" not in session:
        return render_template('home.html', logged_in=False)
    return render_template('home.html', logged_in=True)

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
