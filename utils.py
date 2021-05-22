from client import spotify_client


def get_track_ids(items):
    return [item['track']['id'] for item in items]


def get_playlist_items(playlist_id):
    playlist_len = spotify_client.playlist(playlist_id)['tracks']['total']
    playlist_items = []

    for offset in range(0, playlist_len, 100):
        playlist_items += spotify_client.playlist_items(playlist_id, offset=offset)['items']

    return playlist_items


def get_user_playlists(user_id):
    return spotify_client.user_playlists(user_id)['items']


def get_playlist_ids(playlists):
    return [playlist['id'] for playlist in playlists]


def get_playlist_names(playlists):
    return [playlist['name'] for playlist in playlists]


def exclude(full_list, excluded_list):
    return [item for item in full_list if item not in excluded_list]


def get_playlist_track_ids(playlist_ids):
    track_ids = []
    for playlist_id in playlist_ids:
        track_ids += get_track_ids(get_playlist_items(playlist_id))

    return track_ids


def add_tracks_to_playlist(playlist_id, tracks):
    for i in range(0, len(tracks), 100):
        spotify_client.playlist_add_items(playlist_id, tracks[i: i + 100])


def clear_playlist(playlist_id):
    track_ids = get_track_ids(get_playlist_items(playlist_id))
    for i in range(0, len(track_ids), 100):
        spotify_client.playlist_remove_all_occurrences_of_items(playlist_id, track_ids[i: i + 100])


def move_n_tracks_to_top(n, playlist_id):
    track_ids = get_track_ids(get_playlist_items(playlist_id))
    playlist_len = len(track_ids)
    spotify_client.playlist_reorder_items(playlist_id,
                                          range_start=playlist_len - n,
                                          insert_before=0,
                                          range_length=n)


def playlist_name_to_id(user_id, playlist_name):
    user_playlists = get_user_playlists(user_id)

    playlist_names = get_playlist_names(user_playlists)
    playlist_ids = get_playlist_ids(user_playlists)

    name_to_id_dict = dict(zip(playlist_names, playlist_ids))

    return name_to_id_dict[playlist_name]
