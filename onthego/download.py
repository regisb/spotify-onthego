from __future__ import print_function

from glob import glob
import os
import subprocess

import onthego.youtube

def audio(track_name, artist, directory,
        skip_existing=True, convert_to_mp3=True):

    artist = artist.encode("utf-8")
    track_name = track_name.encode("utf-8")
    if should_skip(track_name, artist, directory, skip_existing, convert_to_mp3):
        print("++ Skipping %s - %s" % (artist, track_name))
        return

    print("++ Processing %s - %s" % (artist, track_name))
    audio_file_path = onthego.youtube.download_to_tmp(track_name, artist)
    if audio_file_path is None:
        print("---- No You Tube video found for '%s - %s'" % (artist, track_name))
        return

    convert_or_copy(audio_file_path, directory, track_name, artist, convert_to_mp3)

def should_skip(track_name, artist, directory, skip_existing, convert_to_mp3):
    if skip_existing:
        if convert_to_mp3 and audio_file_is_already_downloaded(directory, track_name, artist, ".mp3"):
            return True
        elif not convert_to_mp3 and audio_file_is_already_downloaded(directory, track_name, artist, ".*"):
            return True
    return False

def audio_file_is_already_downloaded(directory, track_name, artist, extension):
    pattern = get_audio_file_path(directory, track_name, artist, extension)
    return len(glob(pattern)) > 0

def get_audio_file_path(directory, track_name, artist, extension):
    return os.path.join(directory, "%s - %s%s" % (artist, track_name, extension))

def convert(src_path, dst_path):
    subprocess.call(["avconv", "-v", "quiet", "-i", src_path, dst_path])
    os.remove(src_path)

def convert_or_copy(audio_file_path, directory, track_name, artist, convert_to_mp3):
    ensure_directory_exists(directory)
    if convert_to_mp3:
        dst_path = get_audio_file_path(directory, track_name, artist, ".mp3")
        remove_file(dst_path)
        convert(audio_file_path, dst_path)
    else:
        extension = os.path.splitext(audio_file_path)[1]
        dst_path = get_audio_file_path(directory, track_name, artist, extension)
        remove_file(dst_path)
        os.rename(audio_file_path)

def ensure_directory_exists(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
