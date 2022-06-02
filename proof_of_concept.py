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
    tools = [t for t in timestamps if "Protocol" in t or "Tool" in t]
    return tools


def timestamp_in_seconds(timestamp: str):
    h, m, s = [int(i) for i in timestamp.split(":")]
    return h * 3600 + m * 60 + s


def get_tool_data(description: str):
    lines = description.splitlines()
    timestamps = [l for l in lines if re.match(r"^\d{2}:\d{2}:\d{2}", l)]
    tool_data = [
        dict(
            timestamp=timestamp_in_seconds(re.match(r"^\d{2}:\d{2}:\d{2}", t).group(0)),
            description=re.sub(r"^\d{2}:\d{2}:\d{2}", "", t),
        )
        for t in timestamps
        if "Tool" in t or "Protocol" in t or "Ways to" in t
    ]
    return tool_data


def episode_rundown(video_data: dict):
    description = video_data["snippet"]["description"]
    tool_data = get_tool_data(description)
    return dict(
        title=video_data["snippet"]["title"],
        tools=[
            dict(
                **td,
                link=f"https://www.youtube.com/watch?v={video_data['snippet']['resourceId']['videoId']}&t={td['timestamp']}",
            )
            for td in tool_data
        ],
    )


def rundown_in_txt():
    videos = get_playlist_video_data()
    rundowns = [episode_rundown(v) for v in videos["items"]]
    with open("rundown.md", "w") as f:
        for r in rundowns:
            f.write(f"* ## {r['title']}\n")
            for t in r["tools"]:
                f.write(f"\t* {t['description']} : {t['link']}\n")
    return rundowns


if __name__ == "__main__":
    rundown_in_txt()
    videos = get_playlist_video_data()
    video_data = next((i for i in videos["items"]), None)
    rundown = episode_rundown(video_data)
    print(rundown["title"])
    for r in rundown["tools"]:
        print(f"{r['description']} - {r['link']}")
