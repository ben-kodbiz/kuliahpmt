import yt_dlp
import re
import json
import requests
from bs4 import BeautifulSoup
import os
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

SEARCH_QUERY = config.get('youtube', 'search_queries').split(',')[0] + " playlist"  # Default to first query + " playlist"
MIN_VIDEOS = config.getint('youtube', 'playlist_min_videos')

def get_search_results(query):
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch YouTube search page: {response.status_code}")
    return response.text

def extract_playlist_ids(html):
    # regex matches playlist?list=PLxxxxx pattern
    playlist_ids = list(set(re.findall(r'playlist\?list=([a-zA-Z0-9_-]+)', html)))
    return playlist_ids

def get_playlist_info(playlist_id):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
        'dump_single_json': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/playlist?list={playlist_id}", download=False)
        count = len(info.get('entries', []))
        return {
            "title": info.get("title"),
            "url": f"https://www.youtube.com/playlist?list={playlist_id}",
            "uploader": info.get("uploader"),
            "video_count": count
        }

def main():
    html = get_search_results(SEARCH_QUERY)
    playlist_ids = extract_playlist_ids(html)
    print(f"Found {len(playlist_ids)} potential playlists.")

    results = []
    for pid in playlist_ids:
        try:
            info = get_playlist_info(pid)
            if info["video_count"] >= MIN_VIDEOS:
                results.append(info)
        except Exception as e:
            print(f"Skipping playlist {pid}: {e}")

    # Create data directory if it doesn't exist
    data_dir = config.get('general', 'data_dir')
    os.makedirs(data_dir, exist_ok=True)
    
    with open(os.path.join(data_dir, "playlists_filtered.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()