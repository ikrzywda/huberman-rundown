from config import settings
import requests
import json
import re


def get_huberman_data():
    response = requests.get(
        f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={settings.YT_CHANNEL_ID}&key={settings.YOUTUBE_API_KEY}"
    )
    print(json.dumps(response.json(), sort_keys=True, indent=4))


def get_playlist_video_data():
    request_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={settings.YT_PLAYLIST_ID}&maxResults=1000&key={settings.YOUTUBE_API_KEY}"
    response = requests.get(request_url)
    return response.json()


def get_description_data():
    videos = get_playlist_video_data()
    descriptions = [i["snippet"]["description"] for i in videos["items"]]
    return descriptions


def get_tool_timestamps(description):
    lines = description.splitlines()
    timestamps = [l for l in lines if re.match(r"^\d{2}:\d{2}:\d{2}", l)]
    tools = [t for t in timestamps if "Tool" in t]
    return tools


if __name__ == "__main__":
    description = get_description_data()[0]
    tools = get_tool_timestamps(description)
    for t in tools:
        print(t)
