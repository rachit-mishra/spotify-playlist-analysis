
import sys
import spotipy
import spotipy.util as util
import os
from json.decoder import JSONDecodeError
import json 
import pandas as pd

def authentication():
    username = sys.argv[1]
    client_id = '97b72e4133f3495c88c50016f4ac3347'
    client_secret = '3bb3891a7a68420a817cdd9a5a2a5552'
    redirect_uri = 'http://localhost:8888/callback'
    scope = 'user-library-read'
    try:
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    return username, token 

def retrieve_playlist_content(playlist_id):
    """
    Retrieving the content from each playlist
    """
    playlist_ids = []
    song_content = []
    count = 0  
    username, token = authentication()
    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        playlist_content = sp.user_playlist_tracks(username, playlist_id, limit = 100, fields = None)

        song_content.append(playlist_content['items'])
        if playlist_content['next'] is not None:
            count+=1
        else:
            exit
        with open('{}-{}'.format(username,playlist_id), 'w') as write_dumps:
            json.dump(song_content, write_dumps)
    else:
        print("Unable to retrieve token for: ", username)    

    return sp, song_content, playlist_content , playlist_ids


"""
Method to process the audio features 
for songs in the playlist
"""
def features_processing(playlist_id):
    sp, playlists,playlist_content,playlist_ids = retrieve_playlist_content(playlist_id)
    username, token = authentication()
    playlist_ids = []   
    song_content = []
    count = 0
    list_features = []
    i=0
    #print(playlist_ids)
    if token: 
        playlist_content = sp.user_playlist_tracks(username, playlist_id, limit = 100, fields = None)
        song_content+=playlist_content['items']
        if playlist_content['next'] is not None:
            count+=1
        else:
            exit
        for song in song_content:
            #print(song['track']['id'])
            playlist_ids.append(song['track']['id'])
        while i < len(playlist_ids):
            list_features += sp.audio_features(playlist_ids[i:i+1])
            i+=1

        print(list_features)

    else:
        print("Unable to retrieve token for: ", username)    
    
    return list_features

def write_to_file(playlist_id):
    list_features = features_processing(playlist_id)

    processed_features = []
    """
    Writing audio features to a dataframe
    """
    for features in list_features:
        processed_features.append([features['energy'],
        features['liveness'],
                              features['tempo'], features['speechiness'],
                              features['acousticness'], features['instrumentalness'],
                              features['time_signature'], features['danceability'],
                              features['key'], features['duration_ms'],
                              features['loudness'], features['valence'],
                              features['mode'], features['type'],features['uri']])
    
    df = pd.DataFrame(processed_features, columns = ['energy',
                                                'liveness','tempo',
                                                'speechiness','acousticness',
                                            'instrumentalness', 'time_signature', 'danceability',
                                            'key', 'duration_ms', 'loudness','valence', 'mode', 'type', 'uri'])
    df.to_csv('{}-{}.csv'.format(username,playlist_id), index=False)


def main(username, playlist):
    #sp, song_content, playlist_content , playlist_ids = retrieve_playlist_content(playlist)
    username, token = authentication()
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    # retrieving playlist
    #print(playlists['items'])
    for check_playlist in playlists['items']:
        #print(playlist)
        #print(check_playlist['name'])
        #print(check_playlist['name'] in playlist)
        if check_playlist['name'] in playlist:
            print("Name: {}, Number of songs: {}, Playlist ID: {} ".
                format(check_playlist['name'].encode('utf8'),
                        check_playlist['tracks']['total'],
                        check_playlist['id']))
            retrieve_playlist_content(check_playlist['id'])
            features_processing(check_playlist['id'])
            write_to_file(check_playlist['id'])

if __name__ == '__main__':
    username = sys.argv[1]
    playlist = sys.argv[2]
    main(username, playlist)
   