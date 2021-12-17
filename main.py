import sys
from argparse import ArgumentParser

from src.modes import *

modes = ('lucky', 'move', 'shuffle', 'top_playlist', 'fork', 'merge', 'group', 'news')


class CLI:
    def __init__(self):
        parser = ArgumentParser(usage='python3 main.py <mode> [<args>]')

        parser.add_argument('mode', choices=modes)

        args = parser.parse_args(sys.argv[1:2])

        try:
            message = getattr(self, args.mode)()
            print(message)
        except ValueError as e:
            print(e)

    @staticmethod
    def lucky():
        parser = ArgumentParser(usage='python3 main.py lucky [-f]')

        parser.add_argument('-f', '--force', action='store_true', help='rebuild the lucky playlist')

        args = parser.parse_args(sys.argv[2:])

        message = update_lucky(args.force)
        return message

    @staticmethod
    def move():
        parser = ArgumentParser(usage='python3 main.py move [-p PLAYLIST_NAME] [-n N]')

        parser.add_argument('-p', '--playlist_name', default=user_config['default_move_playlist_name'], type=str,
                            help='name of the playlist to reorder')
        parser.add_argument('-n', '--n', default=1, type=int, help='how much songs to move to the top')

        args = parser.parse_args(sys.argv[2:])

        message = move_to_top(args.n, args.playlist_name)
        return message

    @staticmethod
    def shuffle():
        parser = ArgumentParser(usage='python3 main.py shuffle <playlist_name>')

        parser.add_argument('playlist_name', default=None, type=str,
                            help='name of the playlist to shuffle')

        args = parser.parse_args(sys.argv[2:])

        message = shuffle(args.playlist_name)
        return message

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

        message = create_top_songs_playlist(args.time_range, args.n, args.playlist_name, args.description)
        return message

    @staticmethod
    def fork():
        parser = ArgumentParser(usage='python3 main.py fork <user_id> <playlist_name>')

        parser.add_argument('owner_id', default=None, type=str, help='id of the user that have the playlist you want')
        parser.add_argument('playlist_name', default=None, type=str, help='playlist to fork')
        parser.add_argument('-n', '--name', default=None, type=str, help='name this playlist')
        parser.add_argument('-d', '--description', default=None, type=str, help='describe this playlist')

        args = parser.parse_args(sys.argv[2:])

        message = fork_playlist(args.owner_id, args.playlist_name, args.name, args.description)
        return message

    @staticmethod
    def merge():
        parser = ArgumentParser(usage='python3 main.py merge <first_playlist_name> <second_playlist_name>')

        parser.add_argument('first_playlist_name', default=None, type=str,
                            help='playlist in which the other one will be merged')
        parser.add_argument('second_playlist_name', default=None, type=str,
                            help='playlist that will be merged into the base playlist')

        args = parser.parse_args(sys.argv[2:])

        message = merge_playlists(args.base_playlist_name, args.other_playlist_name)
        return message

    @staticmethod
    def group():
        parser = ArgumentParser(
            usage='python3 main.py group <group_name> [-d DESCRIPTION] [-p PLAYLIST_1 PLAYLIST_2 ...]')

        parser.add_argument('group_name', type=str,
                            help='name the group')
        parser.add_argument('-d', '--description', default=None, type=str, help='describe this playlist')
        parser.add_argument('-p', '--playlists', nargs='+', default=None, help='playlists to group')

        args = parser.parse_args(sys.argv[2:])

        message = group_playlists(args.group_name, args.description, args.playlists)
        return message

    @staticmethod
    def news():
        parser = ArgumentParser(usage='python3 main.py news [-f]')

        parser.add_argument('-n', '--n', default=50, type=int, help='number of songs to add to playlist')
        parser.add_argument('-f', '--force', action='store_true', help='rebuild the news playlist')

        args = parser.parse_args(sys.argv[2:])

        message = add_newly_added(args.n, args.force)
        return message


if __name__ == '__main__':
    CLI()
