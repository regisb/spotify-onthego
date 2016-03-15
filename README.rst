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

Usage
-----

Download all songs from 'My Playlist' and save them as mp3::

    spotify-onthego "My Playlist" ./music/myspotifyplaylist/

The Spotify authentication token and credentials will be stored in
~/.local/share/spotify-onthego/

How to contribute
-----------------

See something that's not working for you, or something that you would like to
be included? Just open a PR with your code, or a Github issue where you
describe the feature you would like to have. 

License
-------

This project is licensed under the `GNU General Public License
v3.0 <https://opensource.org/licenses/gpl-3.0.html>`_.
