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
        version='0.0.1',
        description="Download Spotify playlists via YouTube",
        long_description=get_long_description(),
        classifiers=[],
        keywords='',
        author=u"Régis Behmo",
        author_email='regis@behmo.com',
        url='https://github.com/regisb/spotify-onthego',
        license='MIT',
        packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
        include_package_data=True,
        zip_safe=False,
        install_requires=get_requirements(),
        extras_require={
            'test': ['pytest'],
        },
        entry_points={
            'console_scripts': [
                'spotify-onthego = onthego.scripts.cli:download_playlist'
            ]
        },
)
