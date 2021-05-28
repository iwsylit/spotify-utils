from client import spotify_client
from random import sample
from tqdm import tqdm
import os

os.chdir(os.path.dirname(os.path.relpath(__file__)))


def get_playlist_items(playlist_id):
    playlist_len = spotify_client.playlist(playlist_id)['tracks']['total']
    playlist_items = []

    for offset in range(0, playlist_len, 100):
        playlist_items += spotify_client.playlist_items(playlist_id, offset=offset)['items']

    return playlist_items


def get_track_ids(playlist_items):
    return [item['track']['id'] for item in playlist_items]


def get_playlist_track_ids(playlist_ids):
    track_ids = []

    with tqdm(total=len(playlist_ids), desc='getting songs from your playlists', leave=False) as pbar:
        for playlist_id in playlist_ids:
            track_ids += get_track_ids(get_playlist_items(playlist_id))
            pbar.update()

    return track_ids


def add_tracks_to_playlist(playlist_id, track_ids):
    length = len(track_ids)
    with tqdm(total=length, desc='adding new tracks', leave=False) as pbar:
        for i in range(0, length, 100):
            spotify_client.playlist_add_items(playlist_id, track_ids[i: i + 100])
            pbar.update(100)


def delete_tracks_from_playlist(playlist_id, track_ids):
    length = len(track_ids)
    with tqdm(total=length, desc='deleting tracks', leave=False) as pbar:
        for i in range(0, length, 100):
            spotify_client.playlist_remove_all_occurrences_of_items(playlist_id, track_ids[i: i + 100])
            pbar.update(100)


def clear_playlist(playlist_id):
    track_ids = get_track_ids(get_playlist_items(playlist_id))

    with tqdm(total=len(track_ids), desc='clearing lucky playlist', leave=False) as pbar:
        for i in range(0, len(track_ids), 100):
            spotify_client.playlist_remove_all_occurrences_of_items(playlist_id, track_ids[i: i + 100])
            pbar.update(100)


def get_user_playlists(user_id):
    return spotify_client.user_playlists(user_id)['items']


def get_playlist_ids(playlists):
    return [playlist['id'] for playlist in playlists]


def get_playlist_names(playlists):
    return [playlist['name'] for playlist in playlists]


def exclude(full_list, excluded_list):
    return [item for item in full_list if item not in excluded_list]


def create_playlist_name_to_id_dict(user_id):
    user_playlists = get_user_playlists(user_id)

    playlist_names = get_playlist_names(user_playlists)
    playlist_ids = get_playlist_ids(user_playlists)

    name_to_id_dict = dict(zip(playlist_names, playlist_ids))

    return name_to_id_dict


def playlist_name_to_id(playlist_name, playlist_name_to_id_dict):
    if playlist_name not in playlist_name_to_id_dict.keys():
        print(f'"{playlist_name}" playlist does not exist.')
        exit()

    return playlist_name_to_id_dict[playlist_name]


def move_n_tracks_to_top(n, playlist_id):
    if n < 1:
        print(f'I won\'t move less than one song.')
        exit()

    track_ids = get_track_ids(get_playlist_items(playlist_id))
    playlist_len = len(track_ids)

    if n > playlist_len:
        print('Number of songs you want to move is more than there are songs in the playlist,'
              ' it could cause unexpected results, so i refuse to do it.')
        exit()

    for i in [100] * (n // 100) + [n % 100]:  # looks weird, but it is a super-hyper-extra cool engineering decision
        spotify_client.playlist_reorder_items(playlist_id,
                                              range_start=playlist_len - i,
                                              insert_before=0,
                                              range_length=i)


def shuffle_playlist(playlist_id):
    playlist_len = spotify_client.playlist(playlist_id)['tracks']['total']

    positions = sample(range(playlist_len), playlist_len)

    with tqdm(total=playlist_len, desc='shuffling tracks', leave=False) as pbar:
        for p in positions:
            spotify_client.playlist_reorder_items(playlist_id,
                                                  range_start=0,
                                                  insert_before=p,
                                                  range_length=1)
            pbar.update()


def get_user_top_track_ids(time_range, limit):
    top_tracks = spotify_client.current_user_top_tracks(time_range=time_range, limit=limit)['items']
    top_track_ids = [track['id'] for track in top_tracks]

    return top_track_ids


def create_playlist(user_id, playlist_name, description):
    return spotify_client.user_playlist_create(user_id, playlist_name, description=description)


def time_range_to_str(time_range):
    if time_range == 'short_term':
        return 'last month'
    elif time_range == 'medium_term':
        return 'last six months'
    else:
        return 'since opened spotify for the first time'
