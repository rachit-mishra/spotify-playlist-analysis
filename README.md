# spotify-playlist-analysis
Analyzing my personal spotify playlists - Exploratory analysis, predictive analysis suggesting likeable/not-so-likeable songs

**To run the script**,

spark-submit features_processing.py <username> <playlistname> <config_path>

Test>
Spark command to execute this job:

`spark-submit --files /Users/rachitmishra/Documents/projects/spotify-playlist-analysis/config/config.json features_processing.py rachit.mishra94 'A lot of rap songs' config.json`


# My spotify playlists: (used for testing)
1. https://open.spotify.com/playlist/5egszXQsTHlXuapxfGzK79
2. https://open.spotify.com/playlist/1VzO6phA696s1CRvzMCgbQ?si=caCr6dJlSOmt4HzPeNKI2g



# References:
1.https://buildmedia.readthedocs.org/media/pdf/spotipy/latest/spotipy.pdf
2.https://nvbn.github.io/2019/10/14/playlist-analysis/


# Spotify developer API docs:
https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/
