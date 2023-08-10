import os
from dotenv import load_dotenv
from flask import Flask, request, url_for, session, redirect
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import time
from df_tools import gen_df
from sql_tools import azSqlDB
import time
load_dotenv()

cid = os.getenv('client_id')
cst = os.getenv('client_secret')

app = Flask(__name__)
app.secret_key = os.getenv("flaskappsc")
app.config["SESSION_COOKIE_NAME"]  = os.getenv("flaskappcookie")

def get_token():
    token_info = session.get("token_info",None)
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
    short = gen_df(sp,sp.current_user_top_tracks(time_range="short_term",limit = 10)['items'],"short_term")
    medium = gen_df(sp,sp.current_user_top_tracks(limit = 20)['items'])
    large = gen_df(sp,sp.current_user_top_tracks(time_range="long_term",limit = 50)['items'],"long_term")
    data = [short,medium,large]
    sql_tool = azSqlDB()
    for spotifyDF in data:
        sql_tool.sqlRankings(spotifyDF.create_rankings(),spotifyDF.get_name())
        time.sleep(5)
        sql_tool.sqlGenre(spotifyDF.create_genre())
        sql_tool.sqlSnippets(spotifyDF.create_snippet())
        sql_tool.sqlArtist(spotifyDF.create_artist())
        sql_tool.sqlImage(spotifyDF.create_songIMG())
        sql_tool.sqlSongs(spotifyDF.create_songDetails())
    return 'hello'



if __name__ == '__main__':
  app.run(debug=True)