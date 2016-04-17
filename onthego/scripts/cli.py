#! /usr/bin/env python
from __future__ import print_function

import argparse
import sys

import onthego.auth
import onthego.spotify
import onthego.youtube


def download_playlist():
    parser = argparse.ArgumentParser(description="Download the tracks of a Spotify playlist from YouTube")
    parser.add_argument("playlist", help="Name of playlist. E.g: 'Road music'")
    add_common_options_to_parser(parser)
    args = parser.parse_args()

    spotify_client, youtube_downloader = get_clients(args)

    try:
        for track in spotify_client.iter_playlist_tracks(args.playlist.decode('utf-8')):
            youtube_downloader.audio(track)
    except onthego.spotify.PlaylistNotFound as e:
        print("Playlist '%s' was not found. Did you type its name correctly?" % e.playlist_name)
        sys.exit(1)

def download_my_music():
    parser = argparse.ArgumentParser(description="Download the songs from 'Your Music'")
    parser.add_argument("-l", "--limit", type=int, help="Limit to top N songs")
    add_common_options_to_parser(parser)
    args = parser.parse_args()

    spotify_client, youtube_downloader = get_clients(args)

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

def get_clients(args):
    token_dispenser = onthego.auth.TokenDispenser()
    spotify_client = onthego.spotify.Client(token_dispenser.spotify_username,
                                            token_dispenser.spotify_token)
    youtube_downloader = onthego.youtube.Downloader(
        token_dispenser.google_developer_key,
        args.dst.decode('utf-8'),
        skip_existing=(not args.no_skip),
        convert_to_mp3=(not args.no_convert)
    )
    return spotify_client, youtube_downloader

