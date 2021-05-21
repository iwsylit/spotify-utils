from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

scope = 'playlist-modify-public'

auth_manager = SpotifyOAuth(
    client_id='',
    client_secret='',
    redirect_uri='',
    scope=scope
)

spotify_client = Spotify(auth_manager=auth_manager)
