from glob import glob
import os
import sys

import youtube_dl

from . import id3
from . import search


class Downloader:
    def __init__(
        self,
        directory,
        skip_existing=True,
        convert_to_mp3=True,
        audio_format=None,
        interactive=False,
    ):
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
        audio_file_path = self.download_and_convert(track)
        if audio_file_path is None:
            print(
                "---- No You Tube video found for '%s - %s'"
                % (track.artist, track.name)
            )
            return

    def should_skip(self, track):
        glob_extension = ".mp3" if self.convert_to_mp3 else ".*"
        pattern = get_audio_file_path(self.directory, track, glob_extension)
        return len(glob(pattern)) != 0

    def download_and_convert(self, track):
        video_url = search.best_match(track, interactive=self.interactive)
        if video_url is None:
            return None

        # Prepare file path
        # TODO weirdly enough, the destination path template is not taken into account
        # when the postprocessors are enabled
        filename = "{} - {}.%(ext)s".format(track.artist, track.name)
        path_template = os.path.join(self.directory, filename)
        downloader_params = {
            "format": self.audio_format or "bestaudio",
            "outtmpl": path_template,
            "logger": YoutubeDlLogger(),
        }
        if self.convert_to_mp3:
            downloader_params["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
        downloader = youtube_dl.YoutubeDL(params=downloader_params)
        download_info = downloader.extract_info(video_url, download=False)
        downloaded_file_path = downloader.prepare_filename(download_info)

        # Actually download and convert the video
        print("    Downloading %s to %s" % (video_url, downloaded_file_path))
        downloader.download([video_url])

        converted_file_path = downloaded_file_path
        if self.convert_to_mp3:
            converted_file_path = path_template % {"ext": "mp3"}
            id3.tag(converted_file_path, track)

        return converted_file_path


class YoutubeDlLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        sys.stderr.write(msg)
        sys.stderr.write("\n")


def get_audio_file_path(directory, track, extension):
    filename = "%s - %s%s" % (track.artist, track.name, extension)
    return os.path.join(directory, filter_filename(filename))


def ensure_directory_exists(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def filter_filename(filename):
    return filename.replace("/", " ").replace("\\", " ")
