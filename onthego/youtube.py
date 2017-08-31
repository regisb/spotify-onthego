from __future__ import print_function
from __future__ import unicode_literals

from glob import glob
import os
import shutil
import subprocess
import tempfile


from . import id3
from . import search


class Downloader(object):

    def __init__(self, directory, skip_existing=True, convert_to_mp3=True,
                 audio_format=None, interactive=False):
        """
        Args:
            directory (str): output directory
            skip_existing (bool): by default, existing files are skipped
            convert_to_mp3 (bool): by default, downloaded files will be converted to mp3
            audio_format (str): by default, the best audio files will be
                downloaded. Set this option to e.g: "web" or "m4a" to select the
                best audio file only among these formats.
            interactive (bool): Set to True to let the user interactively
                select the best matching Youtube video.
        """

        self.directory = directory
        self.skip_existing = skip_existing
        self.convert_to_mp3 = convert_to_mp3
        self.audio_format = audio_format
        self.interactive = interactive

    def audio(self, track):
        if self.skip_existing and self.should_skip(track):
            print("++ Skipping %s - %s" % (track.artist, track.name))
            return

        print("++ Processing %s - %s" % (track.artist, track.name))
        audio_file_path = self.download_to_tmp(track)
        if audio_file_path is None:
            print("---- No You Tube video found for '%s - %s'" % (track.artist, track.name))
            return

        self.convert_or_copy(audio_file_path, track)

    def should_skip(self, track):
        glob_extension = ".mp3" if self.convert_to_mp3 else ".*"
        pattern = get_audio_file_path(self.directory, track, glob_extension)
        return len(glob(pattern)) != 0

    def convert_or_copy(self, audio_file_path, track):
        ensure_directory_exists(self.directory)
        if self.convert_to_mp3:
            dst_path = get_audio_file_path(self.directory, track, ".mp3")
            remove_file(dst_path)
            convert(audio_file_path, dst_path)
            id3.tag(dst_path, track)
        else:
            extension = os.path.splitext(audio_file_path)[1]
            dst_path = get_audio_file_path(self.directory, track, extension)
            remove_file(dst_path)
            shutil.move(audio_file_path, dst_path)

    def download_to_tmp(self, track):
        video = search.best_match(track, interactive=self.interactive)
        if video is None:
            return None

        # By default, the best audio format is often webm, which is not
        # supported by older versions of avconv.
        best = video.getbestaudio(preftype=self.audio_format or "any")

        tmp_path = get_tmp_path(best)
        print("    Downloading %s to %s" % (video.watchv_url, tmp_path))
        best.download(tmp_path, quiet=True)
        return tmp_path


def get_audio_file_path(directory, track, extension):
    filename = "%s - %s%s" % (track.artist, track.name, extension)
    return os.path.join(directory, filter_filename(filename))

def convert(src_path, dst_path):
    """
    Convert a file to mp3 and remove the original file.
    """
    try:
        subprocess.call(["avconv", "-v", "quiet", "-i", src_path, dst_path])
    except KeyboardInterrupt:
        os.remove(dst_path)
        raise
    os.remove(src_path)

def ensure_directory_exists(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)

def get_tmp_path(result_stream):
    filename = result_stream.title + "." + result_stream.extension
    filename = filter_filename(filename)
    return os.path.join(tempfile.gettempdir(), filename)

def filter_filename(filename):
    return filename.replace('/', ' ').replace('\\', ' ')
