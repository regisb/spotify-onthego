#! /usr/bin/env python
# -*- coding: utf-8 -*-
from codecs import open as codecs_open
from setuptools import setup, find_packages

def get_long_description():
    with codecs_open('README.rst', encoding='utf-8') as f:
        return f.read()

def get_requirements():
    return [line.strip() for line in open("requirements.txt")]

setup(
        name='spotify-onthego',
        version='0.0.2',
        description="Download Spotify playlists via YouTube",
        long_description=get_long_description(),
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Development Status :: 4 - Beta",
            "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
        ],
        keywords='',
        author=u"xabixab",
        author_email='xabier@xabixab.com',
        url='https://github.com/xabixab/spotify-onthego',
        license='GPL',
        packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
        include_package_data=True,
        zip_safe=False,
        install_requires=get_requirements(),
        extras_require={
            'test': ['pytest'],
        },
        entry_points={
            'console_scripts': [
                'spotify-playlist = onthego.scripts.cli:download_playlist',
                'spotify-mymusic = onthego.scripts.cli:download_my_music'
            ]
        },
)
