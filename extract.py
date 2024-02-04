from spotify_etl import recent_play_list
import pandas as pd


# Now lets extract information

song_names = []
song_ids = []
song_popularitys = []
artist_names = []
artist_ids = []
release_date = []
played_at = []
timestamps = []
duration = []
album_name = []
album_id = []


for song in recent_play_list['items']:
    song_names.append(song['track']['name'])
    song_ids.append(song['track']['id'])
    song_popularitys.append(song['track']['popularity'])
    artist_names.append(song['track']['artists'][0]['name'])
    artist_ids.append(song['track']['artists'][0]['id'])
    release_date.append(song['track']['album']['release_date'])
    played_at.append(song['played_at'])
    timestamps.append(song['played_at'][:10])
    duration.append(song['track']['duration_ms'])
    album_name.append(song['track']['album']['name'])
    album_id.append(song['track']['album']['id'])


song_object = {
    'song_name': song_names,
    'song_id': song_ids,
    'song_popularity': song_popularitys,
    'artist_name': artist_names,
    'artist_id': artist_ids,
    'release_date': release_date,
    'played_at': played_at,
    'timestamps': timestamps,
    'duration': duration,
    'album_name': album_name,
    'album_id': album_id,
}

data = pd.DataFrame(song_object, 
    columns = ['song_name','song_id', 'song_popularity',
               'artist_name','release_date', 'played_at',
               'timestamps', 'duration', 'album_name', 'album_id' ])


print(data)