from __future__ import print_function

import os

import tempfile
import gdata.youtube.service
import pafy

def download_to_tmp(track_name, artist):
    swf_url = get_swf_url(track_name, artist)
    if swf_url is None:
        return None
    video = pafy.new(swf_url)
    best = video.getbestaudio()

    tmp_path = get_tmp_path(best)
    print("    Downloading %s to %s" % (swf_url, tmp_path.encode("utf-8")))
    best.download(tmp_path)
    return tmp_path

def get_swf_url(track_name, artist):
    search_query = get_search_query(track_name, artist)
    swf_url = get_first_search_result(search_query)
    return swf_url

def get_search_query(track_name, artist):
    return (track_name + " " + artist).lower()

def get_first_search_result(search_query):
    yt_service = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    try:
        query.vq = search_query.encode("utf-8")
    except UnicodeDecodeError:
        query.vq = search_query
    feed = yt_service.YouTubeQuery(query)
    # return first entry with valid swf url
    for entry in feed.entry:
        if entry.GetSwfUrl() is not None:
            return entry.GetSwfUrl()

def get_tmp_path(result_stream):
    filename = result_stream.title + "." + result_stream.extension
    filename = filename.replace('/', ' ')
    return os.path.join(tempfile.gettempdir(), filename)
