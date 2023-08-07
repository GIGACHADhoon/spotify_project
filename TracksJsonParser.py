import json
import pandas as pd
#specify filename
TOF = "long"
with open(f'{TOF}.json', 'r') as f:
  songs = json.load(f)

song_data = []
for data in songs:
    # get song id
    song_id = data['id']
    # get song name
    song_name = data['name']
    # get artist names
    artists = []
    for artist_object in data['artists']:
        artists.append(artist_object['name'])
    # get album name
    album = data['album']['name']
    # preview url
    song_preview_url = data['preview_url']
    # release date
    release_date = data['album']['release_date']
    # popularity
    popularity = data['popularity']
    song_data.append({'id':song_id,'name':song_name,'artists':','.join(artists),'album':album,'preview_url':song_preview_url,'release_date':release_date,
                     'popularity':popularity})

pd.DataFrame(song_data).to_excel(f'{TOF}top.xlsx',index=False)


song_images = []
for data in songs:
    song_id = data['id']
    for image in data['album']['images']:
        size = f"{image['width']}x{image['height']}"
        song_images.append({'id':song_id,'img_size':size,'img_url':image['url']})
pd.DataFrame(song_images).to_excel(f'{TOF}topimg.xlsx',index=False)
