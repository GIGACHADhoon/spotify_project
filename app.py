import os
from dotenv import load_dotenv
import base64
import requests
from flask import Flask, request, url_for, session, redirect
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import time

load_dotenv()
cid = os.getenv('client_id')
cst = os.getenv('client_secret')

app = Flask(__name__)
app.secret_key = os.getenv("flaskappsc")
app.config["SESSION_COOKIE_NAME"]  = os.getenv("flaskappcookie")

@app.route("/")
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect")
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("getTracks", _external=True))

@app.route("/getTracks")
def getTracks():
    try:
        token_info = get_token()
    except:
        print('user not logged in')
        return redirect("/")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp.current_user_top_tracks()['items']

def get_token():
    token_info = session.get("token_info",None)
    print(token_info)
    if not token_info:
        raise "Exception"
    
    now = int(time.time())
    if (now - token_info['expires_at']) > 60:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=cid,
        client_secret=cst,
        redirect_uri = url_for('redirectPage',_external=True),
        scope="user-top-read"
    )


if __name__ == '__main__':
  app.run(debug=True)