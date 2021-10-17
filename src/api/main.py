from fastapi import FastAPI
import sys; sys.path.append('../'); sys.path.append('../../')
from modes import *
from config import user_config

app = FastAPI()


@app.get('/lucky')
async def lucky(force: bool = False):
    message = update_lucky(force)

    return {'message': message}


@app.get('/move')
async def move(
        playlist_name: str = user_config['default_move_playlist_name'],
        n: int = 1
):
    message = move_to_top(n, playlist_name)

    return {'message': message}


@app.get('/shuffle')
async def shuffle_playlist(playlist_name: str):
    message = shuffle(playlist_name)

    return {'message': message}


@app.get(
    '/top_playlist',
    description='time_range = "short_term" - 1 month, "medium_term" - 6 months, "long_term" - all data'
)
async def top_playlist(
        time_range: str,
        n: int = 50,
        name: str = None,
        description: str = None
):
    message = create_top_songs_playlist(time_range, n, name, description)

    return {'message': message}


@app.get('/fork')
async def fork_playlist(
        owner_id: str,
        playlist_name: str,
        name: str = None,
        description: str = None
):
    message = fork_playlist(owner_id, playlist_name, name, description)

    return {'message': message}


@app.get('/merge')
async def merge(
        first_playlist_name: str,
        second_playlist_name: str
):
    message = merge_playlists(first_playlist_name, second_playlist_name)

    return {'message': message}


@app.get(
    '/group',
    description='playlists - playlist names space separated'
)
async def group(
        group_name: str,
        description: str = None,
        playlists: str = None
):
    if playlists:
        playlists = playlists.split()
    message = group_playlists(group_name, description, playlists)

    return {'message': message}


@app.get('/news')
async def news(force: bool = False):
    message = add_newly_added(force)

    return {'message': message}
