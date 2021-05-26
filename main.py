from argparse import ArgumentParser
from config import config
from utils import *
import sys


user_id = config['user_id']
lucky_playlist_name = config['default_lucky_playlist_name']
excluded_playlist_names = config['excluded_playlist_names']
default_move_playlist_name = config['default_move_playlist_name']


class CLI:
    def __init__(self):
        parser = ArgumentParser()

        parser.add_argument('mode', help='"lucky", "move" or "shuffle" - which utility you want to use')

        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.mode):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        getattr(self, args.mode)()

    @staticmethod
    def lucky():
        parser = ArgumentParser()

        parser.add_argument('-f', '--force', action='store_true', help='clear the lucky playlist before update')

        args = parser.parse_args(sys.argv[2:])

        update_lucky(args.force)

    @staticmethod
    def move():
        parser = ArgumentParser()

        parser.add_argument('-p', '--playlist_name', default=None, type=str,
                            help='name of the playlist to reorder')
        parser.add_argument('-n', '--n', default=1, type=int, help='how much songs to move to the top')

        args = parser.parse_args(sys.argv[2:])

        move_to_top(args.n, args.playlist_name)

    @staticmethod
    def shuffle():
        parser = ArgumentParser()

        parser.add_argument('-p', '--playlist_name', default=None, type=str,
                            help='name of the playlist to reorder')

        args = parser.parse_args(sys.argv[2:])

        shuffle(args.playlist_name)


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
    if not playlist_name:
        playlist_name = default_move_playlist_name

    playlist_id = playlist_name_to_id(user_id, playlist_name)

    move_n_tracks_to_top(n, playlist_id)


def shuffle(playlist_name):
    playlist_id = playlist_name_to_id(user_id, playlist_name)

    shuffle_playlist(playlist_id)


if __name__ == '__main__':
    CLI()
