
import sys
import spotipy
import spotipy.util as util
import os
from json.decoder import JSONDecodeError
import json 
import pandas as pd
import json

from pyspark import SparkContext, SparkFiles
from pyspark.sql import SQLContext
from pyspark.sql import HiveContext
from pyspark import SparkConf

"""
Setting Spark Configurations
"""
################### Defining spark context/python conf ###############
sc = SparkContext()
sc.setLogLevel("WARN")
sqlContext = HiveContext(sc)

os.environ['PYSPARK_PYTHON'] = '/usr/local/bin/python3'
################### Defining spark context/python conf ###############


def authentication(username):
    conf_file_path = SparkFiles.get(sys.argv[3])
    
    with open(conf_file_path, 'r') as file:
        conf_file = json.load(file)
        #print(conf_file)
    
    
    client_id = conf_file["access_credentials"]["client_id"]
    client_secret = conf_file["access_credentials"]["client_secret"]
    redirect_uri = conf_file["access_credentials"]["redirect_uri"]
    scope = conf_file["access_credentials"]["scope"]
    
    try:
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    except (AttributeError, JSONDecodeError):
        #os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    return token 

def retrieve_playlist_content(username, playlist_id):
    """
    Retrieving the content from each playlist
    """
    playlist_ids = []
    song_content = []
    count = 0  
    token = authentication(username)
    song_names = []
    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        playlist_content = sp.user_playlist_tracks(username, playlist_id, limit = 100, fields = None)
        
        """
        Logic to return tracks in a playlist
        """
        # for tracks in playlist_content['items']:
        #     count+=1
        # print(count)
            #print(tracks['track'])
        #     song_names.append(tracks['track']['name'])
        # print(song_names)
        song_content.append(playlist_content['items'])
        if playlist_content['next'] is not None:
            count+=1
        else:
            exit
        
    else:
        print("Unable to retrieve token for: ", username)    

    return sp, song_content, playlist_content , playlist_ids


def features_processing(username, playlist_id, playlist_name):
    """
    Method to process the audio features 
    for songs in the playlist
    """
    sp, song_content,playlist_content,playlist_ids = retrieve_playlist_content(username, playlist_id)
    token = authentication(username)
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

        #print(list_features)

    else:
        print("Unable to retrieve token for: ", username)    
    
    return list_features

def write_to_file(username, playlist_id, playlist_name):
    list_features = features_processing(username,playlist_id, playlist_name)
    processed_features = []
    """
    Writing audio features to a dataframe
    """
    for features in list_features:
        processed_features.append([features['energy'],
        features['liveness'],features['tempo'], features['speechiness'],features['acousticness'], features['instrumentalness'],features['time_signature'], features['danceability'], features['key'], features['duration_ms'],features['loudness'], features['valence'],features['mode'], features['type'],features['uri']])
    
    df = pd.DataFrame(processed_features, columns = ['energy','liveness','tempo','speechiness','acousticness','instrumentalness', 'time_signature', 'danceability','key', 'duration_ms', 'loudness','valence', 'mode', 'type', 'uri'])
    df.to_csv('{}_____{}.csv'.format(username,playlist_name), index=False)
    print(df.head(5))
    return df

"""
Analyzing songs from individual artist - Likeness of individual artists, etc.
"""
def songs_and_artists(sp,username, playlist_id, playlist):
    playlists = sp.user_playlists(username)
    sp, song_content, playlist_content , playlist_ids = retrieve_playlist_content(username, playlist_id)

    artists_and_songs = []
    for check_playlist in playlists['items']:
        if check_playlist['name'] in playlist:
            tracks = playlist_content['items']
            for track in tracks:
                artists_and_songs.append([track['track']['id'],track['track']['artists'][0]['name'],track['track']['name']])
            
            df_artists = pd.DataFrame(artists_and_songs, columns=['Song id', 'Artist name', 'Song Name'])
            print(df_artists.head(10))
    

def main(username, playlist):
    token = authentication(username)
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)

    for check_playlist in playlists['items']:
        if check_playlist['name'] in playlist:
            print("Name: {}, Number of songs: {}, Playlist ID: {} ".
                format(check_playlist['name'].encode('utf8'),
                        check_playlist['tracks']['total'],
                        check_playlist['id']))
            retrieve_playlist_content(username, check_playlist['id'])
            features_processing(username, check_playlist['id'], check_playlist['name'])
            write_to_file(username, check_playlist['id'],check_playlist['name'])
            songs_and_artists(sp,username, check_playlist['id'], check_playlist['name'])

if __name__ == '__main__':
    username = sys.argv[1]
    playlist = sys.argv[2]
    main(username, playlist)
   