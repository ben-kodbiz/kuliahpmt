#!/usr/bin/env python3
"""
Tool to fetch video IDs from YouTube playlists and organize them in ustaz folders.
This tool uses yt-dlp to extract video information from playlists and creates
organized folder structures with video metadata.
"""

import os
import json
import yt_dlp
from pathlib import Path
import configparser

class PlaylistVideoFetcher:
    def __init__(self, config_file='config.ini'):
        """Initialize the fetcher with configuration."""
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # Get base directories from config
        self.base_dir = self.config.get('general', 'base_dir', fallback='/data/work/pmt')
        self.tools_dir = os.path.join(self.base_dir, 'tools')
        self.data_dir = self.config.get('general', 'data_dir', fallback=os.path.join(self.base_dir, 'data'))
        self.ustaz_dirs = {
            'qarni': os.path.join(self.base_dir, 'ustaz', 'qarni'),
            'fadzil': os.path.join(self.base_dir, 'ustaz', 'fadzil'),
            'halim': os.path.join(self.base_dir, 'ustaz', 'halim'),
            'adli': os.path.join(self.base_dir, 'ustaz', 'adli')
        }
        
        # Create ustaz directories if they don't exist
        for ustaz_dir in self.ustaz_dirs.values():
            os.makedirs(ustaz_dir, exist_ok=True)
            
        # Playlist URLs (these should ideally come from a config file)
        self.playlists = {
            'qarni': [
                {
                    'name': '1000_amalan_sunnah',
                    'title': '1000 Amalan Sunnah Sehari-Hari',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu8Y2CuKhUoRId0szziOz9He'
                },
                {
                    'name': 'bacaan_pelik_ganjil',
                    'title': 'Bacaan Pelik & Ganjil Dalam Solat Namun Sahih',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu_VrsuNVH8VqQVbxYLt22wc'
                },
                {
                    'name': '30_teknik_tadabbur',
                    'title': '30 Teknik Tepat Tadabbur Al-Quran',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu_OrjOhwUltHg927qCs5U-1'
                }
            ],
            'fadzil': [
                {
                    'name': 'tafsir_al_quran',
                    'title': 'Tafsir Al-Quran',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu-NAfJmPOVrMWUxvbi6HC8X'
                }
            ],
            'halim': [
                {
                    'name': 'perubatan_tradisional',
                    'title': 'Perubatan Tradisional & Adat Resam Orang Melayu',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu8vaDF8BN63grv7fOAiu4XI'
                }
            ],
            'adli': [
                {
                    'name': 'usul_tafsir',
                    'title': 'Usul Tafsir : Ustaz Adli Saad',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu99hLBQQz2iTUvB92N2T6Nx'
                },
                {
                    'name': 'ustaz_adli_mohd_saad',
                    'title': 'Ustaz Adli Mohd Saad',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu9Y14ahLfwinIp9aOOBeOzf'
                },
                {
                    'name': 'aqidah_islam_manhaj_salaf',
                    'title': 'Ustaz Adli Mohd Saad: Aqidah Islam Manhaj Salaf',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu_B05TVWrh0sd3cfsOlaE4o'
                },
                {
                    'name': 'mengikuti_nabi_dua_wahyu',
                    'title': 'Ustaz Adli Mohd Saad: Mengikuti Nabi ﷺ Di Bawah Skop Dua Wahyu',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu9kpTBNtOBysevIu9Qv2yuI'
                },
                {
                    'name': 'taifah_al_mansurah',
                    'title': 'Ustaz Adli Mohd Saad: Ta\'ifah Al-Mansurah',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu9JJJGYybgDb8wAALB3B3o-'
                },
                {
                    'name': 'aqidah_4_imam_mazhab',
                    'title': 'Ustaz Adli Mohd Saad: Aqidah 4 Imam Mazhab',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu_HYiB9vUtzZWqVjWXjDld7'
                },
                {
                    'name': 'al_itisham_imam_assyatiibi',
                    'title': 'Ustaz Adli Mohd Saad: Al-I\'tisham, Karya Imam Asy-Syatibi',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu-v7V8fJOqZA-TRnb93YyD9'
                },
                {
                    'name': 'sifat_solat_nabi',
                    'title': 'Ustaz Adli Mohd Saad: Sifat Solat Nabi',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu_URXgXoxxTkw_4JhdmISl9'
                },
                {
                    'name': 'taisir_mustolah_al_hadith',
                    'title': 'Ustaz Adli Mohd Saad: Taisir Mustolah al-Hadith',
                    'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu80GBQ2a_Ofl5szAz4q1CUf'
                }
            ]
        }

    def fetch_playlist_videos(self, playlist_url, max_videos=50):
        """
        Fetch video information from a YouTube playlist.
        
        Args:
            playlist_url (str): URL of the YouTube playlist
            max_videos (int): Maximum number of videos to fetch
            
        Returns:
            list: List of video dictionaries with id, title, url
        """
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'skip_download': True,
            'playlist_end': max_videos,
        }
        
        videos = []
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                
                if '_type' in playlist_info and playlist_info['_type'] == 'playlist':
                    entries = playlist_info.get('entries', [])
                    for entry in entries:
                        if entry and 'id' in entry:
                            video_info = {
                                'id': entry['id'],
                                'title': entry.get('title', 'Untitled'),
                                'url': f"https://www.youtube.com/watch?v={entry['id']}",
                                'thumbnail': entry.get('thumbnail', ''),
                                'duration': entry.get('duration', 0),
                                'upload_date': entry.get('upload_date', ''),
                                'view_count': entry.get('view_count', 0)
                            }
                            videos.append(video_info)
                            
        except Exception as e:
            print(f"Error fetching playlist {playlist_url}: {e}")
            
        return videos

    def save_video_metadata(self, ustaz_name, playlist_name, videos):
        """
        Save video metadata to JSON files in the respective ustaz directory.
        
        Args:
            ustaz_name (str): Name of the ustaz
            playlist_name (str): Name of the playlist
            videos (list): List of video dictionaries
        """
        if ustaz_name not in self.ustaz_dirs:
            print(f"Unknown ustaz: {ustaz_name}")
            return
            
        ustaz_dir = self.ustaz_dirs[ustaz_name]
        playlist_dir = os.path.join(ustaz_dir, playlist_name)
        os.makedirs(playlist_dir, exist_ok=True)
        
        # Save playlist metadata
        playlist_metadata = {
            'playlist_name': playlist_name,
            'ustaz': ustaz_name,
            'video_count': len(videos),
            'videos': videos
        }
        
        metadata_file = os.path.join(playlist_dir, f"{playlist_name}_metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(playlist_metadata, f, indent=2, ensure_ascii=False)
            
        # Save individual video files
        for i, video in enumerate(videos, 1):
            video_file = os.path.join(playlist_dir, f"{i:02d}_{video['id']}.json")
            with open(video_file, 'w', encoding='utf-8') as f:
                json.dump(video, f, indent=2, ensure_ascii=False)
                
        print(f"Saved {len(videos)} videos for {ustaz_name}/{playlist_name}")

    def create_html_embeds(self, ustaz_name, playlist_name, videos):
        """
        Create HTML embed code for videos and save to a file.
        
        Args:
            ustaz_name (str): Name of the ustaz
            playlist_name (str): Name of the playlist
            videos (list): List of video dictionaries
        """
        if ustaz_name not in self.ustaz_dirs:
            print(f"Unknown ustaz: {ustaz_name}")
            return
            
        ustaz_dir = self.ustaz_dirs[ustaz_name]
        playlist_dir = os.path.join(ustaz_dir, playlist_name)
        os.makedirs(playlist_dir, exist_ok=True)
        
        # Create HTML with embedded videos
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{playlist_name.replace('_', ' ').title()} - {ustaz_name.title()}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f7fa; }}
        .header {{ background: #1976d2; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .video-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .video-card {{ background: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .video-title {{ font-weight: bold; margin-bottom: 10px; color: #333; }}
        .video-embed {{ position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; }}
        .video-embed iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }}
        .video-info {{ margin-top: 10px; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{playlist_name.replace('_', ' ').title()}</h1>
        <p>Videos by Ustaz {ustaz_name.title()}</p>
    </div>
    
    <div class="video-grid">
"""
        
        for i, video in enumerate(videos, 1):
            html_content += f"""        <div class="video-card">
            <div class="video-title">{i}. {video['title']}</div>
            <div class="video-embed">
                <iframe src="https://www.youtube.com/embed/{video['id']}" allowfullscreen></iframe>
            </div>
            <div class="video-info">
                <div>Duration: {self.format_duration(video['duration'])}</div>
                <div>Uploaded: {video['upload_date'][:4]}-{video['upload_date'][4:6]}-{video['upload_date'][6:] if video['upload_date'] else 'N/A'}</div>
                <div>Views: {f"{video['view_count']:,}" if video['view_count'] else 'N/A'}</div>
            </div>
        </div>
"""
        
        html_content += """    </div>
</body>
</html>"""
        
        html_file = os.path.join(playlist_dir, f"{playlist_name}_embedded.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Created HTML embed page for {ustaz_name}/{playlist_name}")

    def format_duration(self, seconds):
        """Format duration in seconds to HH:MM:SS format."""
        if not seconds:
            return "N/A"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

    def process_all_playlists(self):
        """Process all playlists for all ustaz."""
        for ustaz_name, playlists in self.playlists.items():
            print(f"\nProcessing playlists for Ustaz {ustaz_name.title()}")
            print("=" * 50)
            
            for playlist in playlists:
                print(f"\nFetching videos for: {playlist['title']}")
                videos = self.fetch_playlist_videos(playlist['url'])
                
                if videos:
                    print(f"Found {len(videos)} videos")
                    self.save_video_metadata(ustaz_name, playlist['name'], videos)
                    self.create_html_embeds(ustaz_name, playlist['name'], videos)
                else:
                    print("No videos found for this playlist")

    def get_playlist_info_only(self, playlist_url):
        """
        Get basic playlist information without fetching all videos.
        
        Args:
            playlist_url (str): URL of the YouTube playlist
            
        Returns:
            dict: Playlist information
        """
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'skip_download': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'playlist_count': info.get('playlist_count', 0),
                    'url': playlist_url,
                    'id': info.get('id', '')
                }
        except Exception as e:
            print(f"Error getting playlist info: {e}")
            return None

def main():
    """Main function to run the video fetcher."""
    fetcher = PlaylistVideoFetcher()
    
    # Process all playlists
    fetcher.process_all_playlists()
    
    print("\n" + "="*50)
    print("PROCESSING COMPLETE")
    print("="*50)
    print("Video metadata and HTML embeds have been created in respective ustaz folders.")
    print("Check the 'ustaz' directory for organized content.")

if __name__ == "__main__":
    main()