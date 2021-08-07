from src import spoti
from random import sample
from tqdm import tqdm


def get_track_ids(playlist_items):
    return [item['track']['id'] for item in playlist_items]


def get_playlist_ids(playlists):
    return [playlist['id'] for playlist in playlists]


def get_playlist_names(playlists):
    return [playlist['name'] for playlist in playlists]


def exclude(full_list, list_to_exclude):
    return [item for item in full_list if item not in list_to_exclude]


def create_playlist_name_to_id_dict(owner_id):
    user_playlists = spoti.get_user_playlists(owner_id)

    playlist_names = get_playlist_names(user_playlists)
    playlist_ids = get_playlist_ids(user_playlists)

    name_to_id_dict = dict(zip(playlist_names, playlist_ids))

    return name_to_id_dict


def playlist_name_to_id(playlist_name, playlist_name_to_id_dict):
    if playlist_name not in playlist_name_to_id_dict.keys():
        print('"{}" playlist does not exist.'.format(playlist_name))
        exit()

    return playlist_name_to_id_dict[playlist_name]


def get_playlists_track_ids(playlist_ids):
    track_ids = []

    with tqdm(total=len(playlist_ids), desc='getting songs from your playlists', leave=False) as pbar:
        for playlist_id in playlist_ids:
            track_ids += get_track_ids(spoti.get_playlist_items(playlist_id))
            pbar.update()

    return track_ids


def move_n_tracks_to_top(n, playlist_id):
    if n < 1:
        print('I won\'t move less than one song.')
        exit()

    track_ids = get_track_ids(spoti.get_playlist_items(playlist_id))
    playlist_len = len(track_ids)

    if n > playlist_len:
        print('Number of songs you want to move is more than there are songs in the playlist,'
              ' it could cause unexpected results, so i refuse to do that.')
        exit()

    for i in [100] * (n // 100) + [n % 100]:  # looks weird, but it is a super-hyper-extra cool engineering decision
        spoti.reorder_playlist_items(
            playlist_id=playlist_id,
            range_start=playlist_len - i,
            insert_before=0,
            range_length=i
        )


def shuffle_playlist(playlist_id):
    playlist_len = spoti.get_playlist_length(playlist_id)

    positions = sample(range(playlist_len), playlist_len)

    with tqdm(total=playlist_len, desc='shuffling tracks', leave=False) as pbar:
        for p in positions:
            spoti.reorder_playlist_items(
                playlist_id,
                range_start=0,
                insert_before=p,
                range_length=1
            )

            pbar.update()


def time_range_to_str(time_range):
    if time_range == 'short_term':
        return 'last month'
    elif time_range == 'medium_term':
        return 'last six months'
    else:
        return 'since logged in spotify for the first time'