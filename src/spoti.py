from config import spotify_client_config
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from tqdm import tqdm
import os


directory = os.path.dirname(os.path.relpath(__file__))
if directory:
    os.chdir(directory)


auth_manager = SpotifyOAuth(
    client_id=spotify_client_config['client_id'],
    client_secret=spotify_client_config['client_secret'],
    redirect_uri=spotify_client_config['redirect_uri'],
    scope=spotify_client_config['scope']
)

spotify_client = Spotify(auth_manager=auth_manager)


def get_playlist_description(playlist_id):
    return spotify_client.playlist(playlist_id)['description']


def get_playlist_items(playlist_id):
    playlist_len = spotify_client.playlist(playlist_id)['tracks']['total']
    playlist_items = []

    for offset in range(0, playlist_len, 100):
        playlist_items += spotify_client.playlist_items(playlist_id, offset=offset)['items']

    return playlist_items


def add_tracks_to_playlist(playlist_id, track_ids):
    with tqdm(total=len(track_ids), desc='adding new tracks', leave=False) as pbar:
        for i in range(0, len(track_ids), 100):
            spotify_client.playlist_add_items(playlist_id, track_ids[i: i + 100])
            pbar.update(100)


def delete_tracks_from_playlist(playlist_id, track_ids):
    with tqdm(total=len(track_ids), desc='deleting tracks', leave=False) as pbar:
        for i in range(0, len(track_ids), 100):
            spotify_client.playlist_remove_all_occurrences_of_items(playlist_id, track_ids[i: i + 100])
            pbar.update(100)


def clear_playlist(playlist_id):
    track_ids = [item['track']['id'] for item in get_playlist_items(playlist_id)]

    with tqdm(total=len(track_ids), desc='clearing playlist', leave=False) as pbar:
        for i in range(0, len(track_ids), 100):
            spotify_client.playlist_remove_all_occurrences_of_items(playlist_id, track_ids[i: i + 100])
            pbar.update(100)


def get_user_playlists(user_id):
    playlists = []
    for i in range(0, spotify_client.user_playlists(user_id)['total'], 50):
        playlists += spotify_client.user_playlists(user_id, offset=i)['items']

    return playlists


def get_user_top_track_ids(time_range, limit):
    top_tracks = spotify_client.current_user_top_tracks(time_range=time_range, limit=limit)['items']

    return [track['id'] for track in top_tracks]


def create_playlist(user_id, playlist_name, description):
    return spotify_client.user_playlist_create(user_id, playlist_name, description=description)


def get_user_name(user_id):
    return spotify_client.user(user_id)['display_name']


def reorder_playlist_items(playlist_id, range_start, insert_before, range_length):
    spotify_client.playlist_reorder_items(playlist_id,
                                          range_start=range_start,
                                          insert_before=insert_before,
                                          range_length=range_length)


def get_playlist_length(playlist_id):
    return spotify_client.playlist(playlist_id)['tracks']['total']
