from __future__ import print_function

from glob import glob
import os
import subprocess
import tempfile

import apiclient.discovery
import pafy


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class Downloader(object):

    def __init__(self, google_developer_key, skip_existing=True, convert_to_mp3=True):

        self.client = apiclient.discovery.build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=google_developer_key
        )
        self.google_developer_key = google_developer_key
        self.skip_existing = skip_existing
        self.convert_to_mp3 = convert_to_mp3

    def audio(self, track_name, artist, directory):
        if self.skip_existing and self.should_skip(track_name, artist, directory):
            print("++ Skipping %s - %s" % (artist, track_name))
            return

        print("++ Processing %s - %s" % (artist, track_name))
        audio_file_path = self.download_to_tmp(track_name, artist)
        if audio_file_path is None:
            print("---- No You Tube video found for '%s - %s'" % (artist, track_name))
            return

        self.convert_or_copy(audio_file_path, directory, track_name, artist)

    def should_skip(self, track_name, artist, directory):
        if self.convert_to_mp3 and self.audio_file_is_already_downloaded(directory, track_name, artist, ".mp3"):
            return True
        elif not self.convert_to_mp3 and self.audio_file_is_already_downloaded(directory, track_name, artist, ".*"):
            return True
        return False

    def audio_file_is_already_downloaded(self, directory, track_name, artist, extension):
        pattern = get_audio_file_path(directory, track_name, artist, extension)
        return len(glob(pattern)) > 0

    def convert_or_copy(self, audio_file_path, directory, track_name, artist):
        ensure_directory_exists(directory)
        if self.convert_to_mp3:
            dst_path = get_audio_file_path(directory, track_name, artist, ".mp3")
            remove_file(dst_path)
            convert(audio_file_path, dst_path, metadata={
                "artist": artist,
                "title": track_name
            })
        else:
            extension = os.path.splitext(audio_file_path)[1]
            dst_path = get_audio_file_path(directory, track_name, artist, extension)
            remove_file(dst_path)
            os.rename(audio_file_path, dst_path)


    def download_to_tmp(self, track_name, artist):
        video_id = self.get_video_id(track_name, artist)
        if video_id is None:
            return None
        video_url = "https://www.youtube.com/watch?v={}".format(video_id)
        video = pafy.new(video_url)
        best = video.getbestaudio()

        tmp_path = get_tmp_path(best)
        print("    Downloading %s to %s" % (video_url, tmp_path))
        best.download(tmp_path, quiet=True)
        return tmp_path

    def get_video_id(self, track_name, artist):
        search_query = (track_name + " " + artist).lower()
        feed = self.client.search().list(
            q=search_query.encode("utf-8"),
            type="video",
            part="id,snippet"
        ).execute()
        # return first entry with valid video id
        for entry in feed["items"]:
            return entry["id"]["videoId"]


def get_audio_file_path(directory, track_name, artist, extension):
    return os.path.join(directory, "%s - %s%s" % (artist, track_name, extension))

def convert(src_path, dst_path, metadata=None):
    cmd = ["avconv", "-v", "quiet", "-i", src_path]
    if metadata:
        for key, val in metadata.iteritems():
            cmd += ['-metadata', '{}={}'.format(key, val.encode('utf-8'))]
    cmd.append(dst_path)

    subprocess.call(cmd)
    os.remove(src_path)

def ensure_directory_exists(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)

def get_tmp_path(result_stream):
    filename = result_stream.title + "." + result_stream.extension
    filename = filename.replace('/', ' ')
    return os.path.join(tempfile.gettempdir(), filename)
