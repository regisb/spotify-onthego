#! /usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open as codecs_open
from setuptools import setup

def get_long_description():
    with codecs_open('README.rst', encoding='utf-8') as f:
        return f.read()

def get_requirements():
    return [line.strip() for line in open("requirements.txt")]

setup(
    name='spotify-onthego',
    version='1.0.3',
    description="Download Spotify songs and playlists (with YouTube)",
    long_description=get_long_description(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
    ],
    keywords='spotify youtube download playlist music songs',
    author=u"Régis Behmo",
    author_email='nospam@behmo.com',
    url='https://github.com/regisb/spotify-onthego',
    license='GPL',
    packages=['onthego'],
    install_requires=[
        "appdirs",
        "eyeD3<0.9",
        "oauth2client==2.0.1",
        "google-api-python-client==1.5.0",
        "spotipy==2.3.8",
        "pafy",
        "pathlib",
        "six",
        "youtube-dl"
    ],
    entry_points={
        'console_scripts': [
            'spotify-playlist = onthego.cli:download_playlist',
            'spotify-mymusic = onthego.cli:download_my_music'
        ]
    },
)
