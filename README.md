# spotify-playlist-analysis
Analyzing my personal spotify playlists - Exploratory analysis, predictive analysis suggesting likeable/not-so-likeable songs

To run the script,

python3 testfile.py <username> <playlistname>

Test:
python3 testfile.py rachit.mishra94 "Mary Jane"

My spotify playlist: https://open.spotify.com/playlist/5egszXQsTHlXuapxfGzK79

References:
1.https://buildmedia.readthedocs.org/media/pdf/spotipy/latest/spotipy.pdf

Spotify developer API docs:
https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/


python3 features_processing.py rachit.mishra94 "HATE ISN'T A STRONG WORD"


Spark command to execute this job:
spark-submit features_processing.py rachit.mishra94 "HATE ISN'T A STRONG WORD" /Users/rachitmishra/Documents/projects/spotify-playlist-analysis/config/config.json
