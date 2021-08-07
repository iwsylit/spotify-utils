from config import user_config
from json import load, dump
from src.utils import *
from src import spoti
import os


playlist_name_to_id_dict = create_playlist_name_to_id_dict(user_config['user_id'])


def update_lucky(force):
    lucky_playlist_id = playlist_name_to_id(user_config['lucky_playlist_name'], playlist_name_to_id_dict)
    excluded_playlist_ids = list(map(lambda n: playlist_name_to_id(n, playlist_name_to_id_dict),
                                     user_config['excluded_playlist_names']))
    excluded_playlist_ids.append(lucky_playlist_id)

    if force:
        spoti.clear_playlist(lucky_playlist_id)

    lucky_playlist_items = spoti.get_playlist_items(lucky_playlist_id)
    lucky_playlist_track_ids = get_track_ids(lucky_playlist_items)

    user_playlist_ids = get_playlist_ids(spoti.get_user_playlists(user_config['user_id']))
    considered_playlist_ids = exclude(user_playlist_ids, excluded_playlist_ids)

    unique_track_ids = set(get_playlists_track_ids(considered_playlist_ids))

    tracks_to_add = exclude(unique_track_ids, lucky_playlist_track_ids)
    tracks_to_delete = exclude(lucky_playlist_track_ids, unique_track_ids)

    spoti.add_tracks_to_playlist(lucky_playlist_id, tracks_to_add)
    spoti.delete_tracks_from_playlist(lucky_playlist_id, tracks_to_delete)

    print('Your lucky playlist has been updated.')


def move_to_top(n, playlist_name):
    playlist_id = playlist_name_to_id(playlist_name, playlist_name_to_id_dict)

    move_n_tracks_to_top(n, playlist_id)

    if n == 1:
        print('1 song of "{}" playlist has been moved to the top.'.format(playlist_name))
    else:
        print('{} songs of "{}" playlist have been moved to the top.'.format(n, playlist_name))


def shuffle(playlist_name):
    playlist_id = playlist_name_to_id(playlist_name, playlist_name_to_id_dict)

    shuffle_playlist(playlist_id)

    print('"{}" playlist has been shuffled.'.format(playlist_name))


def create_top_songs_playlist(time_range, n, playlist_name, description):
    if n < 1:
        print('I won\'t add less then one song to the playlist')
        exit()

    if n > 50:
        print('That\'s too much songs, master. I\'ll put only 50 of them in the playlist.')
        n = 50

    if not playlist_name:
        playlist_name = 'top songs'
    if not description:
        description = f'{n} songs i listened the most {time_range_to_str(time_range)}'

    top_track_ids = spoti.get_user_top_track_ids(time_range, n)

    playlist_id = spoti.create_playlist(user_config['user_id'], playlist_name, description)['id']

    spoti.add_tracks_to_playlist(playlist_id, top_track_ids)

    print('{} top playlist containing {} songs has been created.'.format(time_range, n))


def fork_playlist(owner_id, playlist_name, name, description):
    playlist_id = playlist_name_to_id(playlist_name, create_playlist_name_to_id_dict(owner_id))

    tracks_to_add = get_track_ids(spoti.get_playlist_items(playlist_id))

    if not name:
        name = playlist_name
    if not description:
        description = '{} // playlist i\'ve stolen from {}'.format(spoti.get_playlist_description(playlist_id), spoti.get_user_name(owner_id))

    new_playlist_id = spoti.create_playlist(user_config['user_id'], name, description)['id']

    spoti.add_tracks_to_playlist(new_playlist_id, tracks_to_add)

    print('"{}" playlist was stolen.'.format(playlist_name))


def merge_playlists(first_playlist_name, second_playlist_name):
    base_playlist_id = playlist_name_to_id(first_playlist_name, playlist_name_to_id_dict)
    other_playlist_id = playlist_name_to_id(second_playlist_name, playlist_name_to_id_dict)

    base_playlist_tracks = get_track_ids(spoti.get_playlist_items(base_playlist_id))
    other_playlist_tracks = get_track_ids(spoti.get_playlist_items(other_playlist_id))
    tracks_to_add = base_playlist_tracks + other_playlist_tracks

    new_playlist_id = spoti.create_playlist(
        user_config['user_id'],
        '{} + {}'.format(first_playlist_name, second_playlist_name),
        '"{}" and "{}" together'.format(first_playlist_name, second_playlist_name)
    )['id']

    spoti.add_tracks_to_playlist(new_playlist_id, tracks_to_add)

    print('"{}" and "{}" was merged.'.format(first_playlist_name, second_playlist_name))


def group_playlists(group_name, description, playlists):
    if os.path.exists('.groups'):
        with open('.groups') as f:
            groups = load(f)
    else:
        groups = {}

    if group_name in groups.keys():
        playlist_ids = list(map(lambda n: playlist_name_to_id(n, playlist_name_to_id_dict),
                                groups[group_name]['playlists']))
        group_id = groups[group_name]['group_id']

        group_track_ids = get_track_ids(spoti.get_playlist_items(group_id))
        unique_groupped_track_ids = set(get_playlists_track_ids(playlist_ids))

        tracks_to_add = exclude(unique_groupped_track_ids, group_track_ids)
        tracks_to_delete = exclude(group_track_ids, unique_groupped_track_ids)

        spoti.add_tracks_to_playlist(group_id, tracks_to_add)
        spoti.delete_tracks_from_playlist(group_id, tracks_to_delete)

        print('{} group has been updated.'.format(group_name))
    else:
        if not playlists:
            print('Have not found this group. Specify playlist names to group them.')
            exit()
        if not description:
            description = 'group of the {} playlists'.format(', '.join(playlists))

        playlist_ids = list(map(lambda n: playlist_name_to_id(n, playlist_name_to_id_dict), playlists))
        group_id = spoti.create_playlist(user_config['user_id'], group_name, description)['id']

        spoti.add_tracks_to_playlist(group_id, list(set(get_playlists_track_ids(playlist_ids))))

        groups[group_name] = {
            'group_id': group_id,
            'playlists': playlists
        }

        with open('.groups', 'w') as f:
            dump(groups, f, indent=4)

        print('{} group has been created. To update it you can use "main.py group {}" '
              'command without additional parameters'.format(group_name, group_name))
