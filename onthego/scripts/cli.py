#! /usr/bin/env python
from __future__ import print_function

import argparse
from fnmatch import fnmatch
import os
import sys

import onthego.auth
import onthego.spotify
import onthego.youtube


def download_playlist():
    parser = argparse.ArgumentParser(description="Download the tracks of a Spotify playlist from YouTube")
    parser.add_argument("playlist", help="Name of playlist. E.g: 'Road music'")
    add_common_options_to_parser(parser)
    args = parser.parse_args()

    spotify_client = onthego.spotify.Client()

    playlist_found = False
    for playlist_id, playlist_name, playlist_owner_id in spotify_client.iter_playlists():
        dst = None
        if playlist_name == args.playlist:
            # Exact match: don't create subdirectory
            dst = args.dst
        elif fnmatch(playlist_name, args.playlist):
            # Wildcard match: save in subdirectory
            dst = os.path.join(args.dst, playlist_name.encode('utf-8'))
        if dst is not None:
            playlist_found = True
            print("Downloading playlist '%s' (id=%s) from owner '%s'" % (
                playlist_name, playlist_id, playlist_owner_id)
            )
            youtube_downloader = onthego.youtube.Downloader(
                dst.decode('utf-8'),
                skip_existing=not args.no_skip,
                convert_to_mp3=not args.no_convert
            )
            for track in spotify_client.iter_playlist_tracks(playlist_id, playlist_owner_id):
                youtube_downloader.audio(track)
    if not playlist_found:
        print("Playlist '%s' was not found. Did you type its name correctly?" % args.playlist)
        sys.exit(1)

def download_my_music():
    parser = argparse.ArgumentParser(description="Download the songs from 'Your Music'")
    parser.add_argument("-l", "--limit", type=int, help="Limit to top N songs")
    add_common_options_to_parser(parser)
    args = parser.parse_args()

    spotify_client = onthego.spotify.Client()
    youtube_downloader = onthego.youtube.Downloader(
        args.dst.decode('utf-8'),
        skip_existing=not args.no_skip,
        convert_to_mp3=not args.no_convert
    )

    track_count = 0
    for track in spotify_client.iter_my_music():
        if args.limit is not None and track_count >= args.limit:
            break
        youtube_downloader.audio(track)
        track_count += 1

def add_common_options_to_parser(parser):
    parser.add_argument("-S", "--no-skip", action='store_true',
            help="Don't skip files that were already downloaded.")
    parser.add_argument("-C", "--no-convert", action='store_true',
            help="Don't convert audio files to mp3 format.")
    parser.add_argument("dst", help="Destination directory")
