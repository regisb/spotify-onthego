-----------------
Spotify On The Go
-----------------

A utility to download Spotify playlist tracks from YouTube.


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

    pip install git+git://github.com/regisb/spotify-onthego.git

If you wish to convert the downloaded files to mp3 format, you will need to
install avconv.

For Debian/Ubuntu installation::

    sudo apt-get install avconv

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

Usage
-----

Download all songs from 'My Playlist' and save them as mp3::

    spotify-onthego "My playlist" ./music/myspotifyplaylist/

The Spotify authentication token and credentials will be stored in
~/.local/share/spotify-onthego/
