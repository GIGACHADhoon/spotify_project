import pandas as pd

class gen_df:

    def __init__(self,sp,json_data):
        self.json_data = json_data
        self.sp = sp

    def create_rankings(self):
        rank_data = []
        rank = 1
        for data in self.json_data:
            # get song id
            song_id = data['id']
            rank_data.append({'songID':song_id,'rank':rank})
            rank += 1
        return pd.DataFrame(rank_data)
        

    def create_songDetails(self):
        song_data = []
        for data in self.json_data:
            # get song id
            song_id = data['id']
            # get song name
            song_name = data['name']
            # get artist names
            artist_id = data['artists'][0]['id']
            featuring = []
            for artist_object in data['artists'][1:]:
                featuring.append(artist_object['name'])
            # get album name
            album = data['album']['name']
            # release date
            release_date = data['album']['release_date']
            # popularity
            popularity = data['popularity']
            song_data.append({'songID':song_id,'songName':song_name,'artistID':artist_id,
                              'featuring':','.join(featuring),'album':album,'releaseDate':release_date,
                            'popularity':popularity})
        return pd.DataFrame(song_data)
        
    def create_songIMG(self):
        song_images = []
        for data in self.json_data:
            song_id = data['id']
            for image in data['album']['images']:
                dims = f"{image['width']}x{image['height']}"
                song_images.append({'songID':song_id,'imgDims':dims,'imgURL':image['url']})
        return pd.DataFrame(song_images)

    def create_artist(self):
        artist_data = []
        for data in self.json_data: 
            artist = data['artists'][0]['name']
            artist_id = data['artists'][0]['id']
            artist_data.append({'artistID':artist_id,'artistName':artist})
        return pd.DataFrame(artist_data)

    def create_genre(self):
        genre_data = []
        for data in self.json_data: 
            artist_id = data['artists'][0]['id']
            for genre_object in self.sp.artist(artist_id)['genres']:
                genre_data.append({'artistID':artist_id,'genre':genre_object})
        return pd.DataFrame(genre_data)
    
    def create_snippets(self):
        snippets_data = []
        for data in self.json_data: 
            # get song id
            song_id = data['id']
            song_preview_url = data['preview_url']
            snippets_data.append({'songID':song_id,'snippetURL':song_preview_url})
        return pd.DataFrame(snippets_data)