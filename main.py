from argparse import ArgumentParser
from config import config
from utils import *

user_id = config['user_id']
lucky_playlist_id = config['lucky_playlist_id']
excluded_playlist_ids = config['excluded_playlist_ids']


def update_lucky(force=False):
    if force:
        clear_playlist(lucky_playlist_id)

    lucky_playlist_items = get_playlist_items(lucky_playlist_id)
    lucky_playlist_track_ids = get_track_ids(lucky_playlist_items)

    user_playlist_ids = get_user_playlist_ids(user_id)
    considered_playlist_ids = exclude(user_playlist_ids, excluded_playlist_ids)

    all_track_ids = get_all_playlist_track_ids(considered_playlist_ids)
    unique_track_ids = list(set(all_track_ids))
    tracks_to_add = exclude(unique_track_ids, lucky_playlist_track_ids)

    add_tracks_to_playlist(lucky_playlist_id, tracks_to_add)


def move_to_top(n):
    print(n)
    pass


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('mode', help='"lucky" or "move"')
    parser.add_argument('-f', '--force', action='store_true', help='clear lucky playlist')
    parser.add_argument('-n', '--n', default=1, type=int, help='how much songs to move to the top')

    args = parser.parse_args()

    if args.mode == 'lucky':
        update_lucky(args.force)
    if args.mode == 'move':
        move_to_top(args.n)
