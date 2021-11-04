from fastapi import FastAPI
from utils import handle_value_error

import sys; sys.path.append('..')
from src.modes import *
from config import user_config

app = FastAPI()


@app.post('/lucky')
@handle_value_error
async def lucky(force: bool = False):
    message = update_lucky(force)

    return {'message': message}


@app.post('/move')
@handle_value_error
async def move(
        playlist_name: str = user_config['default_move_playlist_name'],
        n: int = 1
):
    message = move_to_top(n, playlist_name)

    return {'message': message}


@app.post('/shuffle')
@handle_value_error
async def shuffle_playlist(playlist_name: str):
    message = shuffle(playlist_name)

    return {'message': message}


@app.post(
    '/top_playlist',
    description='time_range = "short_term" - 1 month, "medium_term" - 6 months, "long_term" - all data'
)
@handle_value_error
async def top_playlist(
        time_range: str,
        n: int = 50,
        name: str = None,
        description: str = None
):
    message = create_top_songs_playlist(time_range, n, name, description)

    return {'message': message}


@app.post('/fork')
@handle_value_error
async def fork_playlist(
        owner_id: str,
        playlist_name: str,
        name: str = None,
        description: str = None
):
    message = fork_playlist(owner_id, playlist_name, name, description)

    return {'message': message}


@app.post('/merge')
@handle_value_error
async def merge(
        first_playlist_name: str,
        second_playlist_name: str
):
    message = merge_playlists(first_playlist_name, second_playlist_name)

    return {'message': message}


@app.post(
    '/group',
)
@handle_value_error
async def group(
        group_name: str,
        description: str = None,
        playlists: str = None
):
    """
    :param playlists: space separated playlists names
    """
    if playlists:
        playlists = playlists.split()
    message = group_playlists(group_name, description, playlists)

    return {'message': message}


@app.post('/news')
@handle_value_error
async def news(n: int = 50, force: bool = False):
    message = add_newly_added(n, force)

    return {'message': message}
