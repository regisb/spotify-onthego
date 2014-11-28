-----------------
Spotify On The Go
-----------------

A utility to download Spotify playlist tracks from YouTube.


Install requirements
--------------------

Clone the repo::

    git clone https://github.com/regisb/spotify-onthego

Creating a virtualenv is always a good idea::

    virtualenv venv
    source venv/bin/activate

Install dependencies::

    pip install -r requirements.txt

If you wish to convert the downloaded files to mp3 format, you will need to
install avconv::

    sudo apt-get install avconv

Note that you will need valid Spotify app credentials. If you don't have a
valid client ID/secret pair of keys, you can create a Spotify app `here
<https://developer.spotify.com/my-applications/#!/applications/create>`_.

Usage
-----

Download all songs from 'My Playlist' and save them as mp3::

    spotify-onthego "My playlist" ./music/myspotifyplaylist/

The Spotify authentication token and credentials will be stored in
~/.local/share/spotify-onthego/
