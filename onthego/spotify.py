import spotipy


class Client(object):

    def __init__(self, username, token):
        self.spotify_username = username
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
