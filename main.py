from argparse import ArgumentParser
from config import config
from utils import *

user_id = config['user_id']
lucky_playlist_id = config['lucky_playlist_id']
excluded_playlist_ids = config['excluded_playlist_ids']
move_playlist = config['move_playlist']


def update_lucky(force):
    if force:
        clear_playlist(lucky_playlist_id)

    lucky_playlist_items = get_playlist_items(lucky_playlist_id)
    lucky_playlist_track_ids = get_track_ids(lucky_playlist_items)

    user_playlist_ids = get_playlist_ids(get_user_playlists(user_id))
    considered_playlist_ids = exclude(user_playlist_ids, excluded_playlist_ids)

    all_track_ids = get_playlist_track_ids(considered_playlist_ids)
    unique_track_ids = list(set(all_track_ids))
    tracks_to_add = exclude(unique_track_ids, lucky_playlist_track_ids)

    add_tracks_to_playlist(lucky_playlist_id, tracks_to_add)


def move_to_top(n, playlist_id, playlist_name):
    if playlist_name:
        playlist_id = playlist_name_to_id(user_id, playlist_name)

    move_n_tracks_to_top(n, playlist_id)


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('mode', help='"lucky" or "move"')
    parser.add_argument('-f', '--force', action='store_true', help='clear lucky playlist')
    parser.add_argument('-p', '--playlist', default=move_playlist, type=str, help='id of the playlist to reorder')
    parser.add_argument('-t', '--playlist_name', default=None, type=str, help='name (title) of the playlist to reorder')
    parser.add_argument('-n', '--n', default=1, type=int, help='how much songs to move to the top')

    args = parser.parse_args()

    if args.mode == 'lucky':
        update_lucky(args.force)
    if args.mode == 'move':
        move_to_top(args.n, args.playlist, args.playlist_name)
