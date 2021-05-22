# spotify-utils

Some handy utils for Spotify:
1. Move N songs from the bottom of a specified playlist to the top *(can't live without this function)*
2. Gather songs from all your playlists to a specified *"lucky"* playlist *(to play all your songs randomly)*
3. Shuffle specified playlist.
4. *Something else?*

## Requirements
**Python 3** and **spotipy**, **tqdm** packages have to be installed.

### Connecting to Spotify's API
You have to connect to Spotify's API to use these utils.

Do that once before the first start:
 * Go to the [Spotify dashboard](https://developer.spotify.com/dashboard/applications)
 * Click Create an app
 * Put your Client ID and Client Secret into the client.py file
 * Now click Edit Settings
 * Add http://localhost:8888/callback/ to the Redirect URIs
 * Scroll down and click Save
 * Put the Redirect URI into the client.py file
 * You are now ready to authenticate with Spotify!
   - First time you will be redirected to an official Spotify webpage to ask you for permissions.
   - After accepting the permissions, you'll be redirected to localhost. The redirect URL should be parsed automatically, so now you're done.

You can also change scope in `client.py` file to 'playlist-modify-public playlist-modify-private' in order to handle your private playlists, too.

### Configure

Fill `config.py` file:
 * Fill your user id
 * Create the lucky playlist and fill its name
 * Fill names of the playlists you don't want to be added to the lucky playlist
 * Optionally fill the default playlist for song moving.

## Usage
```python3 main.py mode [-f] [-p PLAYLIST_NAME] [-n N]```

positional arguments:
 * mode = "lucky", "move" or "shuffle" - which utility you want to use

optional arguments:
 * **-f** - clear the lucky playlist before update
 * **-p PLAYLIST_NAME** - name of the playlist to reorder
 * **-n N** - how much songs to move to the top

### examples
 * Add new songs to the lucky playlist
    - ```python3 main.py lucky```
 * Update the lucky playlist from scratch
    - ```python3 main.py lucky -f```
 * Move one song from the bottom to the top of the default playlist
    - ```python3 main.py move```
 * Move three songs from the bottom to the top of the *PLAYLIST_NAME* playlist 
    - ```python3 main.py move -p PLAYLIST_NAME -n 3```
 * Shuffle *PLAYLIST_NAME* playlist
    - ```python3 main.py shuffle -p PLAYLIST_NAME```
