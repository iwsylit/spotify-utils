from config import user_id, lucky_playlist_name, excluded_playlist_names
from utils import *

playlist_name_to_id_dict = create_playlist_name_to_id_dict(user_id)


def update_lucky(force):
    lucky_playlist_id = playlist_name_to_id(lucky_playlist_name, playlist_name_to_id_dict)

    excluded_playlist_names.append(lucky_playlist_name)
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
    if n > 50:
        print('That\'s too much songs, master. I\'ll put only 50 of them in the playlist.')
        n = 50

    if not playlist_name:
        playlist_name = 'top songs'
    if not description:
        description = f'{n} songs i listened the most {time_range_to_str(time_range)}'

    top_track_ids = get_user_top_track_ids(time_range, n)

    playlist_id = create_playlist(user_id, playlist_name, description)['id']

    add_tracks_to_playlist(playlist_id, top_track_ids)

    print(f'{time_range} top playlist containing {n} songs has been created.')


def fork_playlist(owner_id, playlist_name, name, description):
    playlist_id = playlist_name_to_id(playlist_name, create_playlist_name_to_id_dict(owner_id))

    tracks_to_add = get_track_ids(get_playlist_items(playlist_id))

    if not name:
        name = playlist_name
    if not description:
        description = f'{get_playlist_description(playlist_id)} // playlist i\'ve stolen from {get_user_name(owner_id)}'

    new_playlist_id = create_playlist(user_id, name, description)['id']

    add_tracks_to_playlist(new_playlist_id, tracks_to_add)

    print(f'"{playlist_name}" playlist was stolen.')


def merge_playlists(first_playlist_name, second_playlist_name):
    base_playlist_id = playlist_name_to_id(first_playlist_name, playlist_name_to_id_dict)
    other_playlist_id = playlist_name_to_id(second_playlist_name, playlist_name_to_id_dict)

    base_playlist_tracks = get_track_ids(get_playlist_items(base_playlist_id))
    other_playlist_tracks = get_track_ids(get_playlist_items(other_playlist_id))
    tracks_to_add = base_playlist_tracks + other_playlist_tracks

    new_playlist_id = create_playlist(
        user_id,
        f'{first_playlist_name} + {second_playlist_name}',
        f'"{first_playlist_name}" and "{second_playlist_name}" together'
    )['id']

    add_tracks_to_playlist(new_playlist_id, tracks_to_add)

    print(f'"{first_playlist_name}" and "{second_playlist_name}" was merged.')
