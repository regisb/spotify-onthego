-----------------
Spotify On The Go
-----------------

A utility to download tracks from your Spotify account. The tracks are
downloaded from YouTube videos and converted as mp3 files.

Changelog
----------

- 2016-07-09 - Add playlist name wildcard matching
- 2016-04-17 - Add album art to the mp3 file ID3 tags (contribution by @xabixab)
- 2016-03-15 - It is now possible to download the tracks from "Your Music > Songs"! See below for details.

Install requirements
--------------------

Creating a virtualenv is always a good idea::

    virtualenv venv
    source venv/bin/activate

spotify-onthego is for Python 2 only. If Python 3 is the default on your
platform, you should create a virtualenv using python2::

    virtualenv --python python2.7 venv
    source venv/bin/activate

Install from Github::

    pip install git+https://github.com/regisb/spotify-onthego.git

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

Note that you will need valid Spotify app credentials. If you don't have a
valid client ID/secret pair of keys, you can create a Spotify app `here
<https://developer.spotify.com/my-applications/#!/applications/create>`_.

Once you have created a Spotify app, you will also have to add a redirect URI
for this app ("Add URI").

The Spotify authentication token and credentials will be stored in
~/.local/share/spotify-onthego/

Usage
-----

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

Examples
--------

Download all songs from 'My Playlist' and save them as mp3::

    spotify-playlist "My Playlist" ./music/myspotifyplaylist/

Create a cronjob to download your Discover Weekly playlist every monday at 7am::

    0 7 * * 1 /home/username/venv/bin/spotify-playlist "Discover Weekly" /home/username/music/discoverweekly

Download your 30 most recent tracks from "My Music"::

    spotify-mymusic -l 30 ./music/mytracks/

Wildcards are supported, too::

    spotify-playlist "Mixtape*" ./music/

In case of 401 error, this may be caused by a previous authorization token that
did not have the right scope. Just remove the
:code:`~/.local/share/spotify-onthego/spotify.token` file and start the command
again.


How to contribute
-----------------

See something that's not working for you, or something that you would like to
be included? Just open a PR with your code, or a Github issue where you
describe the feature you would like to have. 

License
-------

This project is licensed under the `GNU General Public License
v3.0 <https://opensource.org/licenses/gpl-3.0.html>`_.
