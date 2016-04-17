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
            yield self.api_result_to_track(item["track"])

    def iter_my_music(self):
        offset = 0
        limit = 50
        while True:
            tracks = self.spotify.current_user_saved_tracks(limit=limit, offset=offset)["items"]
            if len(tracks) == 0:
                break
            offset += limit

            for item in tracks:
                yield self.api_result_to_track(item["track"])

    def api_result_to_track(self, api_track_result):
        """Convert a 'track' api object to Track

        Album information is fetched and added to the Track object.
        """
        # fetch album info
        album = self.spotify.album(api_track_result["album"]["id"])
        return Track(api_track_result["name"], api_track_result["artists"], album)

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


class Track(object):

    def __init__(self, name, artists, album):
        self.name = name
        self.album = album
        self.artists = artists

    @property
    def artist(self):
        return self.artists[0]["name"]

    @property
    def album_name(self):
        return self.album["name"]

    @property
    def album_art_url(self):
        return self.album["images"][0]["url"]

    @property
    def album_release_date(self):
        """Note that release dates are encoded in Spotify as '%Y-%m-%d',
        '%Y-%m' or '%Y'. If you wish to obtain just the release year, the first
        4 characters should suffice.
        """
        return self.album['release_date']


class PlaylistNotFound(ValueError):

    def __init__(self, playlist_name):
        super(PlaylistNotFound, self).__init__(playlist_name)
        self.playlist_name = playlist_name
