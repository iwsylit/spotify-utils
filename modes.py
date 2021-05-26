from config import user_id, lucky_playlist_name, excluded_playlist_names
from utils import *

playlist_name_to_id_dict = create_playlist_name_to_id_dict(user_id)


def update_lucky(force):
    lucky_playlist_id = playlist_name_to_id(lucky_playlist_name, playlist_name_to_id_dict)
    excluded_playlist_ids = list(map(lambda n: playlist_name_to_id(n, playlist_name_to_id_dict), excluded_playlist_names))

    if force:
        clear_playlist(lucky_playlist_id)

    lucky_playlist_items = get_playlist_items(lucky_playlist_id)
    lucky_playlist_track_ids = get_track_ids(lucky_playlist_items)

    user_playlist_ids = get_playlist_ids(get_user_playlists(user_id))
    considered_playlist_ids = exclude(user_playlist_ids, excluded_playlist_ids)

    all_track_ids = get_playlist_track_ids(considered_playlist_ids)
    unique_track_ids = set(all_track_ids)

    tracks_to_add = exclude(unique_track_ids, lucky_playlist_track_ids)
    tracks_to_delete = exclude(lucky_playlist_track_ids, unique_track_ids)

    add_tracks_to_playlist(lucky_playlist_id, tracks_to_add)
    delete_tracks_from_playlist(lucky_playlist_id, tracks_to_delete)

    print('Your lucky playlist has been updated.')


def move_to_top(n, playlist_name):
    playlist_id = playlist_name_to_id(playlist_name, playlist_name_to_id_dict)

    move_n_tracks_to_top(n, playlist_id)

    if n == 1:
        print(f'1 song of "{playlist_name}" playlist has been moved to the top.')
    else:
        print(f'{n} songs of "{playlist_name}" playlist have been moved to the top.')


def shuffle(playlist_name):
    playlist_id = playlist_name_to_id(playlist_name, playlist_name_to_id_dict)

    shuffle_playlist(playlist_id)

    print(f'"{playlist_name}" playlist has been shuffled.')


def create_top_songs_playlist(time_range, n, playlist_name, description):
    if n < 1:
        print('I won\'t add less then one song to the playlist')

    if not playlist_name:
        playlist_name = 'top songs'

    if not description:
        description = f'{n} songs i listened the most {time_range_to_str(time_range)}'

    top_track_ids = get_user_top_track_ids(time_range, n)

    playlist_id = create_playlist(user_id, playlist_name, description)['id']

    add_tracks_to_playlist(playlist_id, top_track_ids)

    print(f'{time_range} top playlist containing {n} songs has been created.')
