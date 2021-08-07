from argparse import ArgumentParser
from config import user_config
from src.modes import *
import sys


class CLI:
    def __init__(self):
        parser = ArgumentParser(usage='python3 main.py <mode> [<args>]')

        parser.add_argument('mode', choices=["lucky", "move", "shuffle", "top_playlist", "fork", "merge"])

        args = parser.parse_args(sys.argv[1:2])

        getattr(self, args.mode)()

    @staticmethod
    def lucky():
        parser = ArgumentParser(usage='python3 main.py lucky [-f]')

        parser.add_argument('-f', '--force', action='store_true', help='rebuild the lucky playlist')

        args = parser.parse_args(sys.argv[2:])

        update_lucky(args.force)

    @staticmethod
    def move():
        parser = ArgumentParser(usage='python3 main.py move [-p PLAYLIST_NAME] [-n N]')

        parser.add_argument('-p', '--playlist_name', default=user_config['default_move_playlist_name'], type=str,
                            help='name of the playlist to reorder')
        parser.add_argument('-n', '--n', default=1, type=int, help='how much songs to move to the top')

        args = parser.parse_args(sys.argv[2:])

        move_to_top(args.n, args.playlist_name)

    @staticmethod
    def shuffle():
        parser = ArgumentParser(usage='python3 main.py shuffle <playlist_name>')

        parser.add_argument('playlist_name', default=None, type=str,
                            help='name of the playlist to shuffle')

        args = parser.parse_args(sys.argv[2:])

        shuffle(args.playlist_name)

    @staticmethod
    def top_playlist():
        parser = ArgumentParser(usage='python3 main.py top_playlist <playlist_name>')

        parser.add_argument('-t', '--time_range', default='short_term', type=str,
                            help='"short_term" - 1 month, "medium_term" - 6 months, "long_term" - all data',
                            choices=["short_term", "medium_term", "long_term"])
        parser.add_argument('-n', '--n', default=30, type=int,
                            help='how much songs add to the playlist (up to 50)')
        parser.add_argument('-p', '--playlist_name', default=None, type=str, help='how to call this top playlist')
        parser.add_argument('-d', '--description', default=None, type=str, help='describe your top playlist')

        args = parser.parse_args(sys.argv[2:])

        create_top_songs_playlist(args.time_range, args.n, args.playlist_name, args.description)

    @staticmethod
    def fork():
        parser = ArgumentParser(usage='python3 main.py fork <user_id> <playlist_name>')

        parser.add_argument('owner_id', default=None, type=str, help='id of the user that have the playlist you want')
        parser.add_argument('playlist_name', default=None, type=str, help='playlist to fork')
        parser.add_argument('-n', '--name', default=None, type=str, help='name this playlist')
        parser.add_argument('-d', '--description', default=None, type=str, help='describe this playlist')

        args = parser.parse_args(sys.argv[2:])

        fork_playlist(args.owner_id, args.playlist_name, args.name, args.description)

    @staticmethod
    def merge():
        parser = ArgumentParser(usage='python3 main.py merge <first_playlist_name> <second_playlist_name>')

        parser.add_argument('first_playlist_name', default=None, type=str,
                            help='playlist in which the other one will be merged')
        parser.add_argument('second_playlist_name', default=None, type=str,
                            help='playlist that will be merged into the base playlist')

        args = parser.parse_args(sys.argv[2:])

        merge_playlists(args.base_playlist_name, args.other_playlist_name)


if __name__ == '__main__':
    CLI()
