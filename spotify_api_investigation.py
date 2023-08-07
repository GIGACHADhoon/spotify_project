import os
from dotenv import load_dotenv
import base64
from requests import post,get

load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization":"Basic " + auth_base64,
        'Content-Type':'application/x-www-form-urlencoded'
    }

    data = {"grant_type":"client_credentials"}
    result = post(url,headers=headers,data = data)
    return result.json()['access_token']

def get_auth_header(token):
    return {"Authorization":"Bearer "+token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query

    response = get(query_url,headers=headers)
    return response.json()

access_token = get_token()
print(search_for_artist(access_token,"Billy Eilish"))