#!/usr/bin/env python3
"""
Tool to fetch video IDs from Ustaz Ahmad Hasyimi's YouTube playlists.
"""

import os
import json
import yt_dlp
from pathlib import Path
import re

def extract_playlist_id(url):
    """Extract playlist ID from URL."""
    # Match playlist parameter in URL
    match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None

def fetch_ahmadhasyimi_playlist_videos():
    """Fetch videos from Ustaz Ahmad Hasyimi's playlists."""
    
    # Base directory
    base_dir = "/data/work/pmt"
    ustaz_dir = os.path.join(base_dir, "ustaz", "ahmadhasyimi")
    os.makedirs(ustaz_dir, exist_ok=True)
    
    # Ahmad Hasyimi's playlists - original URLs from the text file
    original_urls = [
        'https://www.youtube.com/watch?v=x5186nXFe3U&list=PLv_xoi4FGsu9T74fWm4Hmbu2Ww-kR7nch',
        'https://www.youtube.com/watch?v=M-ijddwYXkw&list=PLv_xoi4FGsu_0O5fYazimItDLv3emBjCf',
        'https://www.youtube.com/watch?v=Rw6FIBZY5Ho&list=PLv_xoi4FGsu_yRAYtjJk6ByMJ__BIuUHK',
        'https://www.youtube.com/watch?v=I6MfEmGXZKs&list=PLv_xoi4FGsu81-F1zhAFTx27ONsh69jP7',
        'https://www.youtube.com/watch?v=a2qnD5kQF3E&list=PLv_xoi4FGsu_1hlB9nhYtsCukB11nuUCX&index=1',
        'https://www.youtube.com/watch?v=csEmgD1wQh8&list=PLv_xoi4FGsu_VUS-ZltcAsajWH0hbGPGF',
        'https://www.youtube.com/watch?v=UhMj6BskKqQ&list=PLv_xoi4FGsu8MrxbymnrzBYZj2iduO0d5',
        'https://www.youtube.com/watch?v=aCYAUFrR6dQ&list=PLv_xoi4FGsu9lpk3ao85FLCsYocpTThEL',
    ]
    
    # Title mappings
    titles = {
        'PLv_xoi4FGsu9T74fWm4Hmbu2Ww-kR7nch': 'Syarah Fikih Dalam Berdoa & Zikir',
        'PLv_xoi4FGsu_0O5fYazimItDLv3emBjCf': 'Syarah Asma\' Husna | Nama Allah SWT & Sifat-Nya',
        'PLv_xoi4FGsu_yRAYtjJk6ByMJ__BIuUHK': 'Tadabbur Surah Al-Insan',
        'PLv_xoi4FGsu81-F1zhAFTx27ONsh69jP7': 'Tadabbur Surah As-Sajdah',
        'PLv_xoi4FGsu_1hlB9nhYtsCukB11nuUCX': 'Tadabbur Surah Al-Mulk',
        'PLv_xoi4FGsu_VUS-ZltcAsajWH0hbGPGF': 'Tadabbur Surah Al-Ma\'idah',
        'PLv_xoi4FGsu8MrxbymnrzBYZj2iduO0d5': 'Syarah 76 Dosa Besar',
        'PLv_xoi4FGsu9lpk3ao85FLCsYocpTThEL': 'Membantah Hujah Golongan Liberal & Pluralisme',
    }
    
    color_options = [
        '#e3f2fd', '#e8f5e9', '#fff3e0', '#f3e5f5', '#e0f2f1',
        '#fbe9e7', '#f1f8e9', '#fff8e1', '#ffebee', '#e1f5fe'
    ]
    
    icon_options = [
        'school', 'menu_book', 'psychology', 'history', 'record_voice_over',
        'wb_sunny', 'favorite', 'stars', 'format_quote', 'block'
    ]
    
    all_playlists_data = {}
    
    for i, original_url in enumerate(original_urls):
        playlist_id = extract_playlist_id(original_url)
        if not playlist_id:
            print(f"Could not extract playlist ID from URL: {original_url}")
            continue
        
        title = titles.get(playlist_id, f"Playlist {playlist_id}")
        name = title.lower().replace(' ', '_').replace("'", '').replace('-', '_').replace('|', '_').replace('/', '_or_')
        color = color_options[i % len(color_options)]
        icon = icon_options[i % len(icon_options)]
        
        # Construct actual playlist URL
        actual_playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
        
        playlist = {
            'name': name,
            'title': title,
            'url': actual_playlist_url,  # Use the actual playlist URL
            'color': color,
            'icon': icon
        }
        
        print(f"Fetching videos from: {playlist['title']}")
        
        # Create directory for this playlist
        playlist_dir = os.path.join(ustaz_dir, playlist['name'])
        os.makedirs(playlist_dir, exist_ok=True)
        
        # Fetch videos using yt-dlp
        ydl_opts = {
            'extract_flat': True,
            'quiet': False,
            'skip_download': True,
            'playlist_end': 50,  # Limit to reasonable number of videos
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist['url'], download=False)
                
                videos = []
                if '_type' in playlist_info and playlist_info['_type'] == 'playlist':
                    entries = playlist_info.get('entries', [])
                    for j, entry in enumerate(entries, 1):
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
                            
                            # Save individual video info
                            video_file = os.path.join(playlist_dir, f"{j:02d}_{entry['id']}.json")
                            with open(video_file, 'w', encoding='utf-8') as f:
                                json.dump(video_info, f, indent=2, ensure_ascii=False)
                
                # Save playlist metadata
                playlist_metadata = {
                    'name': playlist['name'],
                    'title': playlist['title'],
                    'url': playlist['url'],
                    'video_count': len(videos),
                    'videos': videos  # Save all videos for metadata
                }
                
                metadata_file = os.path.join(playlist_dir, f"{playlist['name']}_metadata.json")
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(playlist_metadata, f, indent=2, ensure_ascii=False)
                    
                all_playlists_data[playlist['name']] = playlist_metadata
                print(f"  Saved {len(videos)} videos")
                
                # Create HTML embed page
                create_html_embed_page(playlist_dir, playlist, videos)
                
        except Exception as e:
            print(f"Error fetching playlist {playlist['title']}: {e}")
            # Still create the HTML page even if there are errors
            create_html_embed_page(playlist_dir, playlist, videos)
    
    # Save all playlists data
    all_data_file = os.path.join(ustaz_dir, "all_playlists.json")
    with open(all_data_file, 'w', encoding='utf-8') as f:
        json.dump(all_playlists_data, f, indent=2, ensure_ascii=False)
        
    print(f"\nAll playlists data saved to: {all_data_file}")
    return all_playlists_data

def create_html_embed_page(playlist_dir, playlist, videos):
    """Create an HTML page with embedded YouTube videos."""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{playlist['title']} - Ustaz Ahmad Hasyimi</title>
    <style>
        :root {{
            --primary-color: #1976d2;
            --primary-dark: #1565c0;
            --secondary-color: #f5f5f5;
            --text-primary: #212121;
            --text-secondary: #757575;
            --divider-color: #e0e0e0;
            --white: #ffffff;
            --shadow: 0 2px 4px rgba(0,0,0,0.1);
            --shadow-hover: 0 4px 8px rgba(0,0,0,0.15);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Roboto', Arial, sans-serif; 
            background: #f5f7fa; 
            color: var(--text-primary);
            line-height: 1.6;
        }}

        .header {{ 
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: var(--white); 
            padding: 30px 20px; 
            border-radius: 8px; 
            margin-bottom: 30px;
            box-shadow: var(--shadow);
            text-align: center;
        }}

        .header h1 {{ 
            margin: 0; 
            font-size: 2.2rem;
            font-weight: 500;
        }}

        .header p {{ 
            margin: 10px 0 0 0; 
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .stats {{ 
            display: flex; 
            justify-content: center; 
            gap: 30px; 
            margin: 20px 0;
        }}

        .stat {{ 
            text-align: center; 
        }}

        .stat-value {{ 
            font-size: 1.8rem; 
            font-weight: 500; 
            color: var(--white);
        }}

        .stat-label {{ 
            color: rgba(255,255,255,0.9); 
            font-size: 0.9rem;
        }}

        .back-link {{
            display: inline-block;
            background: rgba(25, 118, 210, 0.08);
            color: var(--primary-color);
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 4px;
            margin-bottom: 30px;
            transition: background 0.3s;
        }}

        .back-link:hover {{
            background: rgba(25, 118, 210, 0.15);
        }}

        .video-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); 
            gap: 25px; 
            margin-top: 20px;
        }}

        .video-card {{ 
            background: var(--white); 
            border-radius: 8px; 
            overflow: hidden; 
            box-shadow: var(--shadow);
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .video-card:hover {{ 
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }}

        .video-title {{ 
            padding: 15px; 
            font-weight: 500; 
            font-size: 1.05rem;
            border-bottom: 1px solid var(--divider-color);
        }}

        .video-embed {{ 
            position: relative; 
            width: 100%; 
            height: 0; 
            padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
        }}

        .video-embed iframe {{ 
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
            border: none;
        }}

        @media (max-width: 768px) {{
            .video-grid {{ 
                grid-template-columns: 1fr; 
            }}
            .header h1 {{ 
                font-size: 1.8rem;
            }}
            .stats {{ 
                gap: 20px;
            }}
            .stat-value {{ 
                font-size: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{playlist['title']}</h1>
            <p>A collection of teachings by Ustaz Ahmad Hasyimi</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{len(videos)}</div>
                    <div class="stat-label">Videos</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{format_duration(sum(v.get('duration', 0) for v in videos))}</div>
                    <div class="stat-label">Total Duration</div>
                </div>
            </div>
        </div>

        <a href="../../../index.html" class="back-link">
            <i class="material-icons" style="vertical-align: middle; font-size: 18px;">arrow_back</i>
            Back to Home
        </a>

        <div class="video-grid">"""
    
    for idx, video in enumerate(videos, 1):
        video_id = video['id']
        title = video['title']
        position = idx
        
        html_content += f'''
            <div class="video-card">
                <div class="video-title">{position}. {title}</div>
                <div class="video-embed">
                    <iframe src="https://www.youtube.com/embed/{video_id}" allowfullscreen></iframe>
                </div>
            </div>'''
    
    html_content += '''
        </div>
    </div>
</body>
</html>'''

    # Write the HTML file
    html_filename = f"{playlist['name']}_embedded.html"
    html_path = os.path.join(playlist_dir, html_filename)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  Created HTML page with {len(videos)} videos")

def format_duration(seconds):
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

def main():
    """Main function."""
    print("Fetching Ustaz Ahmad Hasyimi's YouTube playlist videos...")
    print("=" * 60)
    
    try:
        data = fetch_ahmadhasyimi_playlist_videos()
        print("\n" + "=" * 60)
        print("SUCCESSFULLY FETCHED AHMAD HASYIMI'S VIDEOS!")
        print("=" * 60)
        print("Directories created:")
        for playlist in data.values():
            print(f"- ustaz/ahmadhasyimi/{playlist['name']}/")
        print("\nEach directory contains:")
        print("- Individual video JSON files")
        print("- Playlist metadata JSON")
        print("- HTML page with embedded videos")
        print("\nTo view the videos, open any of the _embedded.html files in a browser.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()