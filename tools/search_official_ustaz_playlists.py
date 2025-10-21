import yt_dlp
import json
import os
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

channel_url = config.get('youtube', 'channel_url') + "/playlists"
base_dir = config.get('general', 'base_dir')
data_dir = config.get('general', 'data_dir')

def get_playlists_from_channel():
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
        'dump_single_json': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        return info.get('entries', [])

def filter_ustaz_playlists(playlists, ustaz_name):
    results = []
    ustaz_name_lower = ustaz_name.lower()
    for p in playlists:
        title = p.get('title', '').lower()
        if ustaz_name_lower in title:
            results.append({
                "title": p.get('title'),
                "url": p.get('url'),
                "video_count": p.get('playlist_count', 0),  # Note: this field might vary
                "uploader": p.get('uploader', 'Unknown')
            })
    return results

def count_videos_in_playlist(playlist_url):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
        'dump_single_json': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            return len(info.get('entries', []))
    except Exception as e:
        print(f"Error counting videos in {playlist_url}: {e}")
        # Return the count from the playlist info if direct count fails
        return 1  # Return 1 as fallback to not lose the playlist

def main():
    playlists = get_playlists_from_channel()
    
    # Get ustaz list from config
    ustaz_list = config.get('youtube', 'search_queries').split(',')
    # Remove 'qarni' as it's handled separately
    ustaz_list = [u for u in ustaz_list if u != 'qarni']
    
    all_results = {}
    
    for ustaz in ustaz_list:
        print(f"\nProcessing {ustaz}...")
        ustaz_playlists = filter_ustaz_playlists(playlists, ustaz)
        
        # Get actual video counts for each playlist
        verified_playlists = []
        for p in ustaz_playlists:
            actual_count = count_videos_in_playlist(p['url'])
            if actual_count >= config.getint('youtube', 'playlist_min_videos'):  # Use config value
                p['video_count'] = actual_count
                verified_playlists.append(p)
                print(f"  Found: {p['title']} ({actual_count} videos)")
        
        all_results[ustaz] = verified_playlists
        print(f"Total {ustaz} playlists with {config.getint('youtube', 'playlist_min_videos')}+ videos: {len(verified_playlists)}")
        
        # Save individual ustaz results
        os.makedirs(data_dir, exist_ok=True)
        with open(os.path.join(data_dir, f"{ustaz}_official_playlists.json"), "w", encoding="utf-8") as f:
            json.dump(verified_playlists, f, indent=2, ensure_ascii=False)
    
    # Save all results combined
    with open(os.path.join(data_dir, "all_ustaz_official_playlists.json"), "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY:")
    for ustaz, playlists in all_results.items():
        print(f"{ustaz}: {len(playlists)} official playlists with >={config.getint('youtube', 'playlist_min_videos')} videos")
    print(f"{'='*60}")
    
    print(json.dumps(all_results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()