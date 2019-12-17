-----------------
Spotify On The Go
-----------------

Download songs and playlist from Spotify. The tracks are downloaded from
YouTube videos and converted as mp3 files.

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
install ffmpeg or avconv.

On Debian/Ubuntu::

    sudo apt-get install ffmpeg

On Mac OS, just follow the instructions from the `official ffmpeg website <https://www.ffmpeg.org/download.html>`__.

Usage
=====

::
    
    $ spotify-playlist -h
    usage: spotify-playlist [-h] [-i] [-S] [-a {webm,ogg,m4a}] [-C] playlist dst

    Download the tracks of a Spotify playlist from YouTube

    positional arguments:
      playlist              Name of playlist. E.g: 'Road music'
      dst                   Destination directory

    optional arguments:
      -h, --help            show this help message and exit
      -i, --interactive     Interactively select the song to download from
                            Youtube.
      -S, --no-skip         Don't skip files that were already downloaded.
      -a {webm,ogg,m4a}, --audio {webm,ogg,m4a}
                            Preferred audio format to download. By default, the
                            best quality audio format will be downloaded. On some
                            platforms (e.g: Debian Wheezy), the default ffmpeg
                            utility does not support audio conversion from webm,
                            so you should specify a different value here. Note
                            that this audio file will eventually be converted to
                            mp3 (unless you specify --no-convert)
      -C, --no-convert      Don't convert audio files to mp3 format.

::

    $ spotify-mymusic -h
    usage: spotify-mymusic [-h] [-l LIMIT] [-i] [-S] [-a {webm,ogg,m4a}] [-C] dst

    Download the songs from 'Your Music'

    positional arguments:
      dst                   Destination directory

    optional arguments:
      -h, --help            show this help message and exit
      -l LIMIT, --limit LIMIT
                            Limit to top N songs
      -i, --interactive     Interactively select the song to download from
                            Youtube.
      -S, --no-skip         Don't skip files that were already downloaded.
      -a {webm,ogg,m4a}, --audio {webm,ogg,m4a}
                            Preferred audio format to download. By default, the
                            best quality audio format will be downloaded. On some
                            platforms (e.g: Debian Wheezy), the default ffmpeg
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

Download favorite songs
------------------------

Download your 30 most recent tracks from "My Music"::

    spotify-mymusic -l 30 ./music/mytracks/

Interactive mode
----------------

By default, ``spotify-onthego`` downloads the first match found on Youtube for
the search ``"<song title> <artist name>"`` (song and artist separated by an
empty space). If you want to manually select the Youtube result to download,
run in interactive mode with the ``-i`` option::

    $ spotify-mymusic -i mymusic/
    ++ Processing Porcupine Tree - Deadwing
    [1] Porcupine Tree - DeadWing https://www.youtube.com/watch?v=GMEwM3YHiME
    [2] Porcupine Tree - Deadwing https://www.youtube.com/watch?v=-Rwp-yvmcRM
    [3] Porcupine Tree - Deadwing [Lyrics on Video] https://www.youtube.com/watch?v=dDepB1mwPhc
    [4] Making of Deadwing https://www.youtube.com/watch?v=ZuYjGfaixDM
    [5] Porcupine Tree- Mellotron Scratch https://www.youtube.com/watch?v=Ag2zXiiuF5Q
    [6] Porcupine Tree - Shesmovedon (Deadwing ver.) https://www.youtube.com/watch?v=OtfJcTBklh8
    [7] Porcupine Tree - Shallow (lyrics) https://www.youtube.com/watch?v=7_8UmXv5Xac
    [8] Porcupine Tree - Arriving Somewhere But Not Here (lyrics on screen) https://www.youtube.com/watch?v=f2ROFnA4HRA
    [9] Porcupine Tree - Deadwing (Lyrics) https://www.youtube.com/watch?v=tMMlEZCaQTY
    [10] Deadwing- Porcupine Tree(Drum Cover) https://www.youtube.com/watch?v=Zb5KTnXGiNU
    Select song to download (default: 1, next=n):

Of course, interactive mode should not be used in automated cron jobs.

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

To setup a development environment, install the ``dev`` requirements::
    
    pip install -r requirements/dev.txt

Code should be `black-formatted <https://black.readthedocs.io/en/stable/>`__. To automatically format your code, run::
    
    make format

Periodically run code lint and formatting tests with:

    make test

License
=======

This project is licensed under the `GNU General Public License
v3.0 <https://opensource.org/licenses/gpl-3.0.html>`_.
