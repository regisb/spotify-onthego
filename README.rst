-----------------
Spotify On The Go
-----------------

Download songs and playlist from Spotify. The tracks are downloaded from
YouTube videos and converted as mp3 files.

Changelog
==========

- 2017-07-13 - v1.0.3:
    - Skip copyrighted videos
    - Fix unicode argument parsing in python 3
- 2017-07-06 - v1.0.0 release! `spotify-onthego` is now compatible with Python 3+.
- 2016-07-09 - Add playlist name wildcard matching
- 2016-04-17 - Add album art to the mp3 file ID3 tags (contribution by @xabixab)
- 2016-03-15 - It is now possible to download the tracks from "Your Music > Songs"! See below for details.

Install
=======

::

    pip install spotify-onthego

Note that you will need valid Spotify app credentials. If you don't have a
valid client ID/secret pair of keys, you can create a Spotify app `here
<https://developer.spotify.com/my-applications/#!/applications/create>`_.

Once you have created a Spotify app, you will also have to add a redirect URI
for this app ("Add URI").

After the first run of the CLI tool, the authentication token and credentials
will be stored in a local configuration file.

Requirements
------------

If you wish to convert the downloaded files to mp3 format, you will need to
install avconv.

For Debian/Ubuntu installation::

    sudo apt-get install libav-tools

For OS X installation you will need to compile from source and you will need to
have gcc installed::

    mkdir avconv
    cd avconv
    wget https://libav.org/releases/libav-11.tar.xz
    tar xjf libav-11.tar.xz
    cd libav-11
    ./configure --disable-yasm
    make install

Usage
=====

::

    $ spotify-playlist -h
    usage: spotify-playlist [-h] [-S] [-a {webm,ogg,m4a}] [-C] playlist dst

    Download the tracks of a Spotify playlist from YouTube

    positional arguments:
      playlist              Name of playlist. E.g: 'Road music'
      dst                   Destination directory

    optional arguments:
      -h, --help            show this help message and exit
      -S, --no-skip         Don't skip files that were already downloaded.
      -a {webm,ogg,m4a}, --audio {webm,ogg,m4a}
                            Preferred audio format to download. By default, the
                            best quality audio format will be downloaded. On some
                            platforms (e.g: Debian Wheezy), the default avconv
                            utility does not support audio conversion from webm,
                            so you should specify a different value here. Note
                            that this audio file will eventually be converted to
                            mp3 (unless you specify --no-convert)
      -C, --no-convert      Don't convert audio files to mp3 format.

::

    $ spotify-mymusic -h
    usage: spotify-mymusic [-h] [-l LIMIT] [-S] [-a {webm,ogg,m4a}] [-C] dst

    Download the songs from 'Your Music'

    positional arguments:
      dst                   Destination directory

    optional arguments:
      -h, --help            show this help message and exit
      -l LIMIT, --limit LIMIT
                            Limit to top N songs
      -S, --no-skip         Don't skip files that were already downloaded.
      -a {webm,ogg,m4a}, --audio {webm,ogg,m4a}
                            Preferred audio format to download. By default, the
                            best quality audio format will be downloaded. On some
                            platforms (e.g: Debian Wheezy), the default avconv
                            utility does not support audio conversion from webm,
                            so you should specify a different value here. Note
                            that this audio file will eventually be converted to
                            mp3 (unless you specify --no-convert)
      -C, --no-convert      Don't convert audio files to mp3 format.

Download playlist
-----------------

Download all songs from 'My Playlist' and save them as mp3::

    spotify-playlist "My Playlist" ./music/myspotifyplaylist/

Create a cronjob to download your Discover Weekly playlist every monday at 7am::

    0 7 * * 1 /home/username/venv/bin/spotify-playlist "Discover Weekly" /home/username/music/discoverweekly

Wildcards are supported, too::

    spotify-playlist "Mixtape*" ./music/

Download favourite songs
------------------------

Download your 30 most recent tracks from "My Music"::

    spotify-mymusic -l 30 ./music/mytracks/

Troubleshooting
===============

In case of 401 error, this may be caused by a previous authorization token that
did not have the right scope. Just remove the
:code:`~/.local/share/spotify-onthego/spotify.token` file and start the command
again.

If mp3 generation fails with an error message related to eyed3, check that your
installed version of eyed3 is at least 0.8::

    $ pip freeze | grep eyeD3
    eyeD3==0.8


Development
===========

See something that's not working for you, or something that you would like to
be included? Just open a `pull request
<https://github.com/regisb/spotify-onthego/pulls>`_ with your code, or a
`Github issue <https://github.com/regisb/spotify-onthego/issues>`_ where you
describe the feature you would like to have. 

License
=======

This project is licensed under the `GNU General Public License
v3.0 <https://opensource.org/licenses/gpl-3.0.html>`_.
