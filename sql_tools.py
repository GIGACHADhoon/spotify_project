import pyodbc
from dotenv import load_dotenv
import os
load_dotenv()
        
class azSqlDB:
    def __init__(self):
        server = os.getenv("server")
        database = os.getenv("database")
        username = os.getenv("username")
        password = os.getenv("password")
        self.conString = 'Driver={ODBC Driver 18 for SQL Server};SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+ \
            ';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;'

    def sqlRankings(self,df,name):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"DROP TABLE IF EXISTS {name}Rankings")
                cursor.execute(f"CREATE TABLE {name}Rankings(songID VARCHAR(22) NOT NULL,ranking TINYINT NOT NULL,PRIMARY KEY(SongID))")
                for _,row in df.iterrows():
                    cursor.execute(f"INSERT INTO {name}Rankings(songID,ranking) VALUES ('{row['songID']}',{row['rank']})")
    
    def sqlGenre(self,df):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"IF NOT EXISTS ( \
                                SELECT * FROM sys.tables t \
                                JOIN sys.schemas s ON (t.schema_id = s.schema_id) \
                                WHERE s.name = 'dbo' AND t.name = 'artistGenres') 	\
                                CREATE TABLE artistGenres (\
                                    artistID VARCHAR(22),\
                                    genre VARCHAR(50));")
                seenArtists = set()
                for artistRow in cursor.execute("SELECT artistID FROM artistGenres").fetchall():
                    if artistRow[0] not in seenArtists:
                        seenArtists.add(artistRow[0])
                for _,row in df.iterrows():
                    if row['artistID'] not in seenArtists:
                        cursor.execute(f"INSERT INTO ArtistGenres(artistID,genre) VALUES ('{row['artistID']}','{row['genre']}')")
    
    def sqlSnippets(self,df):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"IF NOT EXISTS ( \
                                SELECT * FROM sys.tables t \
                                JOIN sys.schemas s ON (t.schema_id = s.schema_id) \
                                WHERE s.name = 'dbo' AND t.name = 'Snippets') 	\
                                CREATE TABLE Snippets (\
                                    songID VARCHAR(22),\
                                    snippetURL TEXT);")
                seensongID = set()
                for songRow in cursor.execute("SELECT songID FROM Snippets").fetchall():
                    if songRow[0] not in seensongID:
                        seensongID.add(songRow[0])
                for _,row in df.iterrows():
                    if row['songID'] not in seensongID:
                        cursor.execute(f"INSERT INTO Snippets(songID,snippetURL) VALUES ('{row['songID']}','{row['snippetURL']}')")
    
    def sqlArtist(self,df):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"IF NOT EXISTS ( \
                                SELECT * FROM sys.tables t \
                                JOIN sys.schemas s ON (t.schema_id = s.schema_id) \
                                WHERE s.name = 'dbo' AND t.name = 'Artist') 	\
                                CREATE TABLE Artist (\
                                    artistID VARCHAR(22),\
                                    artistName VARCHAR(100), PRIMARY KEY(artistID));")
                seenArtists = set()
                for artistRow in cursor.execute("SELECT artistID FROM Artist").fetchall():
                    if artistRow[0] not in seenArtists:
                        seenArtists.add(artistRow[0])
                for _,row in df.iterrows():
                    if row['artistID'] not in seenArtists:
                        cursor.execute(f"INSERT INTO Artist(artistID,artistName) VALUES ('{row['artistID']}','{row['artistName']}')")
                        seenArtists.add(row['artistID'])
    
    def sqlImage(self,df):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"IF NOT EXISTS ( \
                                SELECT * FROM sys.tables t \
                                JOIN sys.schemas s ON (t.schema_id = s.schema_id) \
                                WHERE s.name = 'dbo' AND t.name = 'Images') 	\
                                CREATE TABLE Images (\
                                    songID VARCHAR(22), imgURL TEXT,\
                                    imgDims VARCHAR(50), PRIMARY KEY(songID,imgDims));")
                seenImages = set()
                for imageROW in cursor.execute("SELECT * FROM Images").fetchall():
                    if (imageROW[0],imageROW[2]) not in seenImages:
                        seenImages.add((imageROW[0],imageROW[2]))
                for _,row in df.iterrows():
                    if (row['songID'],row['imgDims']) not in seenImages:
                        cursor.execute(f"INSERT INTO Images(songID,imgURL,imgDims) VALUES ('{row['songID']}','{row['imgURL']}','{row['imgDims']}')")
                        seenImages.add((row['songID'],row['imgDims']))
    
    def sqlSongs(self,df):
        with pyodbc.connect(self.conString) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"IF NOT EXISTS ( \
                                SELECT * FROM sys.tables t \
                                JOIN sys.schemas s ON (t.schema_id = s.schema_id) \
                                WHERE s.name = 'dbo' AND t.name = 'SongDetails') 	\
                                CREATE TABLE SongDetails (\
                                    songID VARCHAR(22), songName NTEXT, \
                                    artistID VARCHAR(22),featuring TEXT, \
                                    album NTEXT,releaseDate DATE, \
                                    popularity TINYINT, PRIMARY KEY(songID));")
                seensongID = set()
                for songRow in cursor.execute("SELECT songID FROM SongDetails").fetchall():
                    if songRow[0] not in seensongID:
                        seensongID.add(songRow[0])
                for _,row in df.iterrows():
                    if row['songID'] not in seensongID:
                        cursor.execute(f"INSERT INTO SongDetails VALUES ('{row['songID']}',N'{row['songName']}','{row['artistID']}','{row['featuring']}',N'{row['album']}','{row['releaseDate']}',{row['popularity']})")