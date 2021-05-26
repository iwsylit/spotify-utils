from config import user_id, lucky_playlist_name, excluded_playlist_names
from utils import *


def update_lucky(force):
    lucky_playlist_id = playlist_name_to_id(user_id, lucky_playlist_name)

    if force:
        clear_playlist(lucky_playlist_id)

    lucky_playlist_items = get_playlist_items(lucky_playlist_id)
    lucky_playlist_track_ids = get_track_ids(lucky_playlist_items)

    user_playlist_ids = get_playlist_ids(get_user_playlists(user_id))
    considered_playlist_ids = exclude(user_playlist_ids, excluded_playlist_names)

    all_track_ids = get_playlist_track_ids(considered_playlist_ids)
    unique_track_ids = list(set(all_track_ids))
    tracks_to_add = exclude(unique_track_ids, lucky_playlist_track_ids)

    add_tracks_to_playlist(lucky_playlist_id, tracks_to_add)


def move_to_top(n, playlist_name):
    playlist_id = playlist_name_to_id(user_id, playlist_name)

    move_n_tracks_to_top(n, playlist_id)


def shuffle(playlist_name):
    playlist_id = playlist_name_to_id(user_id, playlist_name)

    shuffle_playlist(playlist_id)
