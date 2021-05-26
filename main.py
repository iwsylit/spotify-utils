from functions import update_lucky, move_to_top, shuffle
from argparse import ArgumentParser
from config import default_move_playlist_name
import sys


class CLI:
    def __init__(self):
        parser = ArgumentParser()

        parser.add_argument('mode', help='"lucky", "move" or "shuffle"')

        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.mode):
            print(f'"{args.mode}" mode does not exist.')
            parser.print_help()
            exit(1)

        getattr(self, args.mode)()

    @staticmethod
    def lucky():
        parser = ArgumentParser()

        parser.add_argument('-f', '--force', action='store_true', help='rebuild the lucky playlist')

        args = parser.parse_args(sys.argv[2:])

        update_lucky(args.force)

    @staticmethod
    def move():
        parser = ArgumentParser()

        parser.add_argument('playlist_name', default=default_move_playlist_name, type=str,
                            help='name of the playlist to reorder')
        parser.add_argument('n', default=1, type=int, help='how much songs to move to the top')

        args = parser.parse_args(sys.argv[2:])

        move_to_top(args.n, args.playlist_name)

    @staticmethod
    def shuffle():
        parser = ArgumentParser()

        parser.add_argument('playlist_name', default=None, type=str,
                            help='name of the playlist to shuffle')

        args = parser.parse_args(sys.argv[2:])

        shuffle(args.playlist_name)


if __name__ == '__main__':
    CLI()
