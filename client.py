from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

auth_manager = SpotifyOAuth(
    client_id='',
    client_secret='',
    redirect_uri='',
    scope=''
)

spotify_client = Spotify(auth_manager=auth_manager)
