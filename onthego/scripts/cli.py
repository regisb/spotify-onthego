from __future__ import print_function

import argparse
import sys

import onthego.download
import onthego.spotify.auth


def download_playlist():
    parser = argparse.ArgumentParser(description="Download the tracks of a Spotify playlist from YouTube")
    parser.add_argument("-S", "--no-skip", action='store_true',
            help="Don't skip files that were already downloaded.")
    parser.add_argument("-C", "--no-convert", action='store_true',
            help="Don't convert audio files to mp3 format.")
    parser.add_argument("playlist", help="Name of playlist. E.g: 'Road music'")
    parser.add_argument("dst", help="Destination directory")
    args = parser.parse_args()

    spotify_client = onthego.spotify.auth.Client()
    try:
        for track_name, artist in spotify_client.iter_tracks(args.playlist):
            onthego.download.audio(track_name, artist, args.dst,
                skip_existing=(not args.no_skip), convert_to_mp3=(not args.no_convert))
    except onthego.spotify.auth.PlaylistNotFound as e:
        print("Playlist '%s' was not found. Did you type its name correctly?" % e.playlist_name)
        sys.exit(1)
