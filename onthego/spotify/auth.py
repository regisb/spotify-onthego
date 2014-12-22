from __future__ import print_function

import json
import os

import spotipy
import spotipy.util

class TokenDispenser(object):

    def __init__(self):
        self._token = None
        self._credentials = None

    @property
    def token(self):
        if self._token is None:
            token = self.load_token()
            if token is None or not self.is_token_valid(token):
                token = self.get_new_token()
                self.save_token(token)
            self._token = token
        return self._token

    def load_token(self):
        token_path = self.get_token_path()
        if not os.path.exists(token_path):
            return None
        with open(token_path) as token_file:
            return token_file.read().strip()

    def get_new_token(self):
        token = spotipy.util.prompt_for_user_token(self.username,
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope="playlist-read-private")
        return token

    def is_token_valid(self, token):
        try:
            spotify_client = spotipy.Spotify(auth=token)
            spotify_client.current_user()
        except spotipy.client.SpotifyException:
            return False
        return True

    def save_token(self, token):
        token_path = self.get_token_path()
        self.check_directory_exists(token_path)
        with open(token_path, "w") as token_file:
            token_file.write(token)

    @property
    def credentials(self):
        if self._credentials is None:
            try:
                credentials = self.load_credentials()
            except CredentialsNotFound:
                credentials = self.ask_for_credentials()
                self.save_credentials(*credentials)
            self._credentials = credentials
        return self._credentials

    @property
    def username(self):
        return self.credentials[0]
    @property
    def client_id(self):
        return self.credentials[1]
    @property
    def client_secret(self):
        return self.credentials[2]
    @property
    def redirect_uri(self):
        return self.credentials[3]

    def load_credentials(self):
        credentials_path = self.get_credentials_path()
        if not os.path.exists(credentials_path):
            raise CredentialsNotFound()
        try:
            with open(credentials_path) as credentials_file:
                credentials = json.load(credentials_file)
            return (
                credentials["USERNAME"],
                credentials["CLIENT_ID"],
                credentials["CLIENT_SECRET"],
                credentials["REDIRECT_URI"]
            )
        except (ValueError, KeyError):
            print("Could not parse credentials file")
            raise CredentialsNotFound()

    def ask_for_credentials(self):
        print("""You need to register as a developer and create a Spotify app in order to use Spotify On The Go.
You may create an app here: https://developer.spotify.com/my-applications/#!/applications/create
Please enter your app credentials:""")
        username = raw_input("Spotiy username: ")
        client_id = raw_input("Client ID: ")
        client_secret = raw_input("Client secret: ")
        redirect_uri = raw_input("Redirect URI: ")
        return username, client_id, client_secret, redirect_uri

    def save_credentials(self, username, client_id, client_secret, redirect_uri):
        credentials_path = self.get_credentials_path()
        print("Saving Spotify credentials to", credentials_path)
        self.check_directory_exists(credentials_path)
        with open(credentials_path, "w") as credentials_file:
            json.dump({
                "USERNAME": username,
                "CLIENT_ID": client_id,
                "CLIENT_SECRET": client_secret,
                "REDIRECT_URI": redirect_uri,
            }, credentials_file)

    def get_token_path(self):
        return self.get_config_file_path("spotify.token")

    def get_credentials_path(self):
        return self.get_config_file_path("credentials.json")

    def get_config_file_path(self, filename):
        return os.path.join(
                os.path.expanduser("~/.local/share/spotify-onthego/"),
                filename)

    def check_directory_exists(self, path):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

class CredentialsNotFound(Exception):
    pass

class Client(object):

    def __init__(self):
        token_dispenser = TokenDispenser()
        token = token_dispenser.token
        self.spotify_username = token_dispenser.username
        self.spotify = spotipy.Spotify(auth=token)

    def iter_tracks(self, playlist_name):
        playlist_id, playlist_owner = self.get_playlist_id_info(playlist_name)
        print("Downloading playlist '%s' (id=%s) from owner '%s'" % (
            playlist_name, playlist_id, playlist_owner)
        )
        for item in self.spotify.user_playlist(playlist_owner, playlist_id)["tracks"]["items"]:
            track = item["track"]
            yield track["name"], track["artists"][0]["name"]

    def get_playlist_id_info(self, name):
        for playlist_id, playlist_name, playlist_owner in self.iter_playlists():
            if playlist_name == name:
                return playlist_id, playlist_owner
        raise PlaylistNotFound(name)

    def iter_playlists(self):
        offset = 0
        limit = 50
        while True:
            playlists = self.spotify.user_playlists(self.spotify_username, limit=limit, offset=offset)["items"]
            if len(playlists) == 0:
                break
            offset += limit
            for playlist in playlists:
                yield playlist["id"], playlist["name"], playlist['owner']['id']

class PlaylistNotFound(ValueError):

    def __init__(self, playlist_name):
        super(PlaylistNotFound, self).__init__(playlist_name)
        self.playlist_name = playlist_name
