import yt_dlp
import re
import json

channel_url = "https://www.youtube.com/@PROmediaTAJDIDofficial/playlists"
search_keyword = "qarni"

def get_playlists(channel_url):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
        'dump_single_json': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        return info.get('entries', [])

def filter_playlists(playlists, keyword):
    keyword = keyword.lower()
    results = []
    for p in playlists:
        title = p.get('title', '').lower()
        desc = p.get('description', '').lower()
        if keyword in title or keyword in desc:
            results.append(p)
    return results

def count_videos(playlist_url):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
        'dump_single_json': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        return len(info.get('entries', []))

def main():
    playlists = get_playlists(channel_url)
    filtered = filter_playlists(playlists, search_keyword)
    result = []

    for p in filtered:
        url = p.get('url')
        count = count_videos(url)
        if count >= 10:  # Changed from 20 to 10
            result.append({
                "title": p.get('title'),
                "url": url,
                "video_count": count
            })

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()