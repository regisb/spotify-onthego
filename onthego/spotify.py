import spotipy


class Client(object):

    def __init__(self, username, token):
        self.spotify_username = username
        self.spotify = spotipy.Spotify(auth=token)

    def iter_playlist_tracks(self, playlist_name):
        playlist_id, playlist_owner = self.get_playlist_info(playlist_name)
        print("Downloading playlist '%s' (id=%s) from owner '%s'" % (
            playlist_name, playlist_id, playlist_owner)
        )
        for item in self.spotify.user_playlist(playlist_owner, playlist_id)["tracks"]["items"]:
            track = item["track"]
            album = track["track"]["album"]["name"]
            art = track["track"]["album"]["images"][0]["url"]
            year = track["added_at"]
            yield track["name"], track["artists"][0]["name"], album, art, year

    def iter_my_music(self):
        offset = 0
        limit = 50
        while True:
            tracks = self.spotify.current_user_saved_tracks(limit=limit, offset=offset)["items"]
            if len(tracks) == 0:
                break
            offset += limit
            
            for track in tracks:
                album = track["track"]["album"]["name"]
                art = track["track"]["album"]["images"][0]["url"]
                year = self.spotify.album(track["track"]["album"]["id"])["release_date"]
                yield track["track"]["name"], track["track"]["artists"][0]["name"], album, art, year

    def get_playlist_info(self, name):
        """Get playlist ID and owner

        Args:
            name (str)

        Returns:
            playlist_id (str)
            playlist_owner (str)
        """
        for playlist_id, playlist_name, playlist_owner_id in self.iter_playlists():
            if playlist_name == name:
                return playlist_id, playlist_owner_id
        raise PlaylistNotFound(name)

    def iter_playlists(self):
        """Iterate on all user playlists

        Yields:
            playlist_id (str)
            playlist_name (str)
            playlist_owner (str)
        """
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
