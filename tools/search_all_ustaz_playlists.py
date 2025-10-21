import yt_dlp
import re
import json
import requests
from bs4 import BeautifulSoup
import os

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

def search_ustaz_playlists(ustaz_name, min_videos=20):
    search_query = f"{ustaz_name} playlist"
    print(f"Searching for {search_query}...")
    
    html = get_search_results(search_query)
    playlist_ids = extract_playlist_ids(html)
    print(f"Found {len(playlist_ids)} potential playlists for {ustaz_name}.")

    results = []
    for pid in playlist_ids:
        try:
            info = get_playlist_info(pid)
            if info["video_count"] >= min_videos:
                results.append(info)
        except Exception as e:
            print(f"Skipping playlist {pid}: {e}")

    return results

def main():
    ustaz_list = ["adli", "halim", "rizal"]
    all_results = {}
    
    for ustaz in ustaz_list:
        print(f"\n{'='*50}")
        results = search_ustaz_playlists(ustaz)
        all_results[ustaz] = results
        print(f"Found {len(results)} playlists for {ustaz} with >= {20} videos")
        
        # Save individual ustaz results
        os.makedirs("data", exist_ok=True)
        with open(f"data/{ustaz}_playlists_filtered.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Save all results combined
    with open("data/all_ustaz_playlists_filtered.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY:")
    for ustaz, playlists in all_results.items():
        print(f"{ustaz}: {len(playlists)} playlists with >=20 videos")
    print(f"{'='*60}")
    
    print(json.dumps(all_results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()