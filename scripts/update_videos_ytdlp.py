import json, subprocess, os
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'tools', 'config.ini'))

# Get base directory
base_dir = config.get('general', 'base_dir')
data_dir = config.get('general', 'data_dir')

CHANNELS = {
    "qarni": config.get('playlists', 'qarni_url'),  # Ustaz Qarni: 1000 Amalan Sunnah Sehari-Hari
    "fadzil": config.get('playlists', 'fadzil_url'),  # Ustaz Fadzil Kamaruddin: Tafsir Al-Quran
    "halim": config.get('playlists', 'halim_search'),  # Search for Ustaz Halim content
    "adli":  config.get('playlists', 'adli_url'),  # Ustaz Adli: Aqidah Islam Manhaj Salaf
}

def fetch_videos(url, count=10):
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--flat-playlist",
        "--playlist-end", str(count),
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    videos = []
    for line in result.stdout.splitlines():
        item = json.loads(line)
        videos.append({
            "id": item["id"],
            "title": item.get("title", "Untitled"),
            "url": f"https://www.youtube.com/watch?v={item['id']}",
        })
    return videos

def main():
    os.makedirs(data_dir, exist_ok=True)
    for ustaz, url in CHANNELS.items():
        print(f"Fetching {ustaz} videos…")
        try:
            videos = fetch_videos(url)
            with open(os.path.join(data_dir, f"{ustaz}.json"), "w") as f:
                json.dump(videos, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to fetch {ustaz}: {e}")

if __name__ == "__main__":
    main()