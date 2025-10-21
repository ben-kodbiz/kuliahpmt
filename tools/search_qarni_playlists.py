import json, subprocess

SEARCH_URL = "https://www.youtube.com/@PROmediaTAJDIDofficial/search?query=qarni"

def search_playlists(min_videos=20):
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--flat-playlist",
        SEARCH_URL
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    
    playlists = []
    for line in result.stdout.splitlines():
        try:
            item = json.loads(line)
            # Filter only playlists with > min_videos
            if item.get("_type") == "playlist" and item.get("playlist_count", 0) >= min_videos:
                playlists.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "count": item.get("playlist_count"),
                    "id": item.get("id")
                })
        except json.JSONDecodeError:
            continue

    return playlists

if __name__ == "__main__":
    results = search_playlists(min_videos=20)
    print(json.dumps(results, indent=2))