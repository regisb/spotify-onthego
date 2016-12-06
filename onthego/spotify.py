import spotipy

from . import auth

class Client(object):

    def __init__(self):
        token_dispenser = auth.TokenDispenser()
        self.spotify_username = token_dispenser.spotify_username
        self.spotify = spotipy.Spotify(auth=token_dispenser.spotify_token)

    def iter_playlist_tracks(self, playlist_id, playlist_owner_id):
        for item in self._iter_items(self.spotify.user_playlist_tracks, playlist_owner_id, playlist_id):
            yield self.api_result_to_track(item["track"])

    def iter_my_music(self):
        for item in self._iter_items(self.spotify.current_user_saved_tracks):
            yield self.api_result_to_track(item["track"])

    def _iter_items(self, func, *args):
        """
        Iterate over multiple pages of item results
        """
        offset = 0
        limit = 50
        while True:
            items = func(*args, limit=limit, offset=offset)['items']
            if len(items) == 0:
                break
            offset += limit

            for item in items:
                yield item

    def api_result_to_track(self, api_track_result):
        """Convert a 'track' api object to Track

        Album information is fetched and added to the Track object.
        """
        # fetch album info
        album_id = api_track_result["album"]["id"]
        album = None
        if album_id is not None:
	    album = self.spotify.album(album_id)
        return Track(api_track_result["name"], api_track_result["artists"], album)

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

    def __init__(self, name, artists, album={'name': ''}):
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
