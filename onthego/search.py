from apiclient import discovery

from . import auth


def best_match(track, interactive=False):
    return get_video_interactively(track) if interactive else get_video(track)


def get_video_url(video_id):
    return "https://www.youtube.com/watch?v={}".format(video_id)


def get_video(track):
    """Get the video url that best matches the requested track"""
    for video_id, _video_title in iter_search_results(track):
        try:
            return get_video_url(video_id)
        except BlockedVideoError:
            continue


def get_video_interactively(track):
    results = []
    new_results = []
    result = None
    for video_id, video_title in iter_search_results(track):
        new_results.append((get_video_url(video_id), video_title))

        if len(new_results) % 10 == 0:
            result = pick_result(results, new_results)
            if result is not None:
                return result

    while result is None:
        result = pick_result(results, new_results, has_next=False)
    return result


def pick_result(results, new_results, has_next=True):
    for pos, result in enumerate(new_results):
        print("[{}] {} {}".format(pos + len(results) + 1, result[1], result[0]))

    while new_results:
        results.append(new_results.pop(0))

    while True:
        message = "Select song to download (default=1{}): ".format(
            ", next=n" if has_next else ""
        )
        choice = input(message)
        choice = choice.strip().lower()
        if has_next and choice == "n":
            return None
        if not choice:
            choice = "1"
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice <= len(results):
                video_url = results[choice - 1][0]
                try:
                    return video_url
                except BlockedVideoError:
                    print(
                        "Your choice is unavailable in your country of "
                        "origin. Please choose a different source."
                    )

        print("Invalid choice: {}".format(choice))


def iter_search_results(track):
    """Iterate over youtube video ids that match the queried track"""
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    token_dispenser = auth.TokenDispenser()
    client = discovery.build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=token_dispenser.google_developer_key,
    )

    search_query = (track.name + " " + track.artist).lower()
    page_token = None
    while True:
        query = {
            "q": search_query,
            "type": "video",
            "part": "id,snippet",
            "pageToken": page_token,
        }
        feed = client.search().list(**query).execute()  # pylint: disable=no-member

        for entry in feed["items"]:
            video_id = entry["id"]["videoId"]
            video_title = entry["snippet"]["title"]
            if video_id is not None:
                yield video_id, video_title

        page_token = feed.get("nextPageToken")
        if page_token is None:
            break


class BlockedVideoError(Exception):
    pass
