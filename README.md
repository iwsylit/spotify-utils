# spotify-utils

Some handy utils for Spotify:
1. Move N songs from the bottom to the top of a specified playlist
2. Gather songs from all your playlists to a *"lucky"* playlist
3. Shuffle a playlist
4. Create a playlist containing your top songs of all time, the last six months or the last month
5. Fork someone's playlist
6. Merge two playlists
7. Group playlists
8. Gather N songs from all your playlists to a specified *"news"* playlist and order them by date added
9. *Something else?*

It is possible to use these utils via CLI or API.\
The repo comes along with a [Telegram bot](https://github.com/iwsylit/spotify-utils-bot). 

## Requirements
**Python 3** with ***spotipy*** and ***tqdm*** packages.\
If you want to use API, ***fast-api*** is needed.

### Connecting to Spotify's API
You have to connect to Spotify's API to use these utils.

Do that once before the first start:
 * Go to the [Spotify dashboard](https://developer.spotify.com/dashboard/applications)
 * Click Create an app
 * Put your Client ID and Client Secret into the config file
 * Now click Edit Settings
 * Add http://localhost:8888/callback/ to the Redirect URIs
 * Scroll down and click Save
 * Put the Redirect URI into the client.py file
 * You are now ready to authenticate with Spotify!
   - First time you will be redirected to an official Spotify webpage to ask you for permissions.
   - After accepting the permissions, you'll be redirected to localhost. The redirect URL should be parsed automatically, so now you're done.

You can also add "playlist-modify-private" scope in `config.py` file in order to handle your private playlists, too. 
(*probably; i did not test that*)

## Configuration

Fill `config.py` file:
 * Fill your user id
 * Create the lucky playlist and fill its name
 * Fill names of the playlists you don't want to be added to the lucky playlist
 * Optionally fill the default playlist for song moving

## CLI usage
`python3 main.py <mode> [<args>]` 

Possible modes:
 * "lucky" - create a playlist containing all your songs
 * "move" - move n songs from the bottom to the top of a playlist
 * "shuffle" - shuffle songs in a playlist
 * "top_playlist" - create a playlist containing your top songs
 * "fork" - steal someone's playlist
 * "merge" - merge two playlists
 * "group" - group playlists
 * "news" - create a playlist containing all your songs ordered by date added
   
Use `python3 main.py <mode> -h` to see arguments for each mode.

### Examples
 * Add new songs to the lucky playlist
    - `python3 main.py lucky`
 * Move one song from the bottom to the top of the default playlist
    - `python3 main.py move`
 * Move three songs from the bottom to the top of the *PLAYLIST_NAME* playlist 
    - `python3 main.py move -p PLAYLIST_NAME -n 3`
 * Shuffle *PLAYLIST_NAME* playlist
    - `python3 main.py shuffle PLAYLIST_NAME`
 * Create a playlist containing 50 your top songs the last month
    - `python3 main.py top_playlist -t short_term -n 50`
 * Steal my mischmasz playlist:
    - `python3 main.py fork f3ed4n4boipjflbzepw7rffte mischmasz`
 * Create group of *PLAYLIST_NAME_1* and *PLAYLIST_NAME_2* playlists called *GROUP_NAME*:
    - `python3 main.py group GROUP_NAME -p PLAYLIST_NAME_1 PLAYLIST_NAME_2`


## API usage

To run the API use `run.sh` script in `src/api` directory. 
The API is available on `9876` port by default.
See Swagger docs on `0.0.0.0:9876/docs` for more help.

## Docker

To run the API in Docker
1. Build the image `docker build -t spotify-utils .`
2. Run it `docker run -d --name spotify-utils -p 9876:9876 spotify-utils`

Note: do not forget to fill the config file and to authorize in Spotify 
(if you were already authorized, just copy your `src/.cache` before building 
the image)
