#!/usr/bin/env python3
"""
Tool to fetch video IDs from Ustaz Adli's YouTube playlists.
"""

import os
import json
import yt_dlp
from pathlib import Path

def fetch_adli_playlist_videos():
    """Fetch videos from Ustaz Adli's playlists."""
    
    # Base directory
    base_dir = "/data/work/pmt"
    ustaz_dir = os.path.join(base_dir, "ustaz", "adli")
    os.makedirs(ustaz_dir, exist_ok=True)
    
    # Ustaz Adli's playlists
    playlists = [
        {
            'name': 'usul_tafsir',
            'title': 'Usul Tafsir : Ustaz Adli Saad',
            'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu99hLBQQz2iTUvB92N2T6Nx',
            'color': '#e8f5e9',
            'icon': 'menu_book'
        },
        {
            'name': 'ustaz_adli_mohd_saad',
            'title': 'Ustaz Adli Mohd Saad',
            'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu9Y14ahLfwinIp9aOOBeOzf',
            'color': '#e3f2fd',
            'icon': 'collections_bookmark'
        },
        {
            'name': 'aqidah_islam_manhaj_salaf',
            'title': 'Ustaz Adli Mohd Saad: Aqidah Islam Manhaj Salaf',
            'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu_B05TVWrh0sd3cfsOlaE4o',
            'color': '#f3e5f5',
            'icon': 'psychology'
        },
        {
            'name': 'mengikuti_nabi_dua_wahyu',
            'title': 'Ustaz Adli Mohd Saad: Mengikuti Nabi ﷺ Di Bawah Skop Dua Wahyu',
            'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu9kpTBNtOBysevIu9Qv2yuI',
            'color': '#f3e5f5',
            'icon': 'person_pin'
        },
        {
            'name': 'taifah_al_mansurah',
            'title': 'Ustaz Adli Mohd Saad: Ta\'ifah Al-Mansurah',
            'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu9JJJGYybgDb8wAALB3B3o-',
            'color': '#fff3e0',
            'icon': 'group'
        },
        {
            'name': 'aqidah_4_imam_mazhab',
            'title': 'Ustaz Adli Mohd Saad: Aqidah 4 Imam Mazhab',
            'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu_HYiB9vUtzZWqVjWXjDld7',
            'color': '#fce4ec',
            'icon': 'account_balance'
        },
        {
            'name': 'al_itisham_imam_assyatiibi',
            'title': 'Ustaz Adli Mohd Saad: Al-I\'tisham, Karya Imam Asy-Syatibi',
            'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu-v7V8fJOqZA-TRnb93YyD9',
            'color': '#fff3e0',
            'icon': 'school'
        },
        {
            'name': 'sifat_solat_nabi',
            'title': 'Ustaz Adli Mohd Saad: Sifat Solat Nabi',
            'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu_URXgXoxxTkw_4JhdmISl9',
            'color': '#e8f5e9',
            'icon': 'local_mosque'
        },
        {
            'name': 'taisir_mustolah_al_hadith',
            'title': 'Ustaz Adli Mohd Saad: Taisir Mustolah al-Hadith',
            'url': 'https://www.youtube.com/playlist?list=PLv_xoi4FGsu80GBQ2a_Ofl5szAz4q1CUf',
            'color': '#e3f2fd',
            'icon': 'library_books'
        }
    ]
    
    all_playlists_data = {}
    
    for playlist in playlists:
        print(f"Fetching videos from: {playlist['title']}")
        
        # Create directory for this playlist
        playlist_dir = os.path.join(ustaz_dir, playlist['name'])
        os.makedirs(playlist_dir, exist_ok=True)
        
        # Fetch videos using yt-dlp
        ydl_opts = {
            'extract_flat': True,
            'quiet': False,
            'skip_download': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist['url'], download=False)
                
                videos = []
                if '_type' in playlist_info and playlist_info['_type'] == 'playlist':
                    entries = playlist_info.get('entries', [])
                    for i, entry in enumerate(entries, 1):
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
                            video_file = os.path.join(playlist_dir, f"{i:02d}_{entry['id']}.json")
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
    <title>{playlist['title']} - Ustaz Adli Mohd Saad</title>
    <style>
        :root {{
            --primary-color: #9c27b0;
            --primary-dark: #7b1fa2;
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

        .video-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); 
            gap: 25px; 
            margin-top: 20px;
        }}

        .video-card {{ 
            background: var(--white); 
            border-radius: 10px; 
            overflow: hidden; 
            box-shadow: var(--shadow);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .video-card:hover {{ 
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }}

        .video-title {{ 
            padding: 18px 20px 15px; 
            font-weight: 500; 
            font-size: 1.1rem;
            color: var(--text-primary);
            border-bottom: 1px solid var(--divider-color);
        }}

        .video-embed {{ 
            position: relative; 
            padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
            height: 0; 
            overflow: hidden;
        }}

        .video-embed iframe {{ 
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
            border: none;
        }}

        .video-info {{ 
            padding: 15px 20px; 
            background: var(--secondary-color);
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}

        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 500;
            padding: 10px 15px;
            border-radius: 4px;
            background: rgba(156, 39, 176, 0.05);
        }}

        .back-link:hover {{
            background: rgba(156, 39, 176, 0.1);
        }}

        @media (max-width: 768px) {{
            .video-grid {{ 
                grid-template-columns: 1fr; 
            }}
            .header h1 {{ 
                font-size: 1.8rem;
            }}
            .stats {{ 
                flex-direction: column; 
                gap: 10px;
            }}
        }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
</head>
<body>
    <div class="header">
        <h1>{playlist['title']}</h1>
        <p>Ustaz Adli Mohd Saad</p>
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
    
    <div class="video-grid">
"""
    
    for i, video in enumerate(videos, 1):  # Include all videos
        duration_str = format_duration(video.get('duration', 0))
        upload_date = video.get('upload_date', '')
        if upload_date:
            formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
        else:
            formatted_date = "N/A"
            
        html_content += f"""        <div class="video-card">
            <div class="video-title">{i}. {video.get('title', 'Untitled')}</div>
            <div class="video-embed">
                <iframe src="https://www.youtube.com/embed/{video['id']}" allowfullscreen></iframe>
            </div>
            <div class="video-info">
                <span>
                    <i class="material-icons" style="font-size: 16px; vertical-align: middle;">access_time</i>
                    {duration_str}
                </span>
                <span>
                    <i class="material-icons" style="font-size: 16px; vertical-align: middle;">calendar_today</i>
                    {formatted_date}
                </span>
            </div>
        </div>
"""
    
    html_content += """    </div>
</body>
</html>"""
    
    html_file = os.path.join(playlist_dir, f"{playlist['name']}_embedded.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  Created HTML embed page: {html_file}")

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
    print("Fetching Ustaz Adli's YouTube playlist videos...")
    print("=" * 60)
    
    try:
        data = fetch_adli_playlist_videos()
        print("\n" + "=" * 60)
        print("SUCCESSFULLY FETCHED ADLI'S VIDEOS!")
        print("=" * 60)
        print("Directories created:")
        for playlist_name in data.keys():
            print(f"- ustaz/adli/{playlist_name}/")
        print("\nEach directory contains:")
        print("- Individual video JSON files")
        print("- Playlist metadata JSON")
        print("- HTML page with embedded videos")
        print("\nTo view the videos, open any of the _embedded.html files in a browser.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()