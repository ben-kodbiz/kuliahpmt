#!/usr/bin/env python3
"""
Tool to fetch video IDs from Salman's YouTube playlists.
"""

import os
import json
import yt_dlp
from pathlib import Path

def fetch_salman_playlist_videos():
    """Fetch videos from Salman's playlists."""

    # Base directory
    base_dir = "/data/work/pmt"
    ustaz_dir = os.path.join(base_dir, "ustaz", "salman")
    os.makedirs(ustaz_dir, exist_ok=True)

    # Salman's playlists from ustazsalman.txt
    playlists = [
        {
            'name': 'kitab_seerah_nabawiyyah',
            'title': 'Kitab Seerah Nabawiyyah Ar Raheeq Al Makhtum',
            'url': 'https://www.youtube.com/watch?v=gD01wSglxw8&list=PLrv0fyvlN4wmpX3eKQanLts5x4Xl875yY&index=23',
            'color': '#e3f2fd',
            'icon': 'menu_book'
        },
        {
            'name': 'empat_khalifah_rasul',
            'title': 'Kitab Perjalanan Hidup Empat Khalifah Rasul Yang Agung',
            'url': 'https://www.youtube.com/watch?v=U_Y_3wJPLs8&list=PLv_xoi4FGsu9pJIOfNM0sL2pw7exS0fxY',
            'color': '#e8f5e9',
            'icon': 'history'
        },
        {
            'name': 'pengenalan_uluhayah',
            'title': 'Pengenalan ULUHIYAH, RUBUBIYAH & ASMA’ WA SIFAT',
            'url': 'https://www.youtube.com/watch?v=U3EEb0-HnOo&list=PLrv0fyvlN4wl77eZEZXTYkbiFllx6DaaK',
            'color': '#fff3e0',
            'icon': 'psychology'
        },
        {
            'name': 'hadis_40_imam_nawawi',
            'title': 'Hadis 40 Imam Nawawi',
            'url': 'https://www.youtube.com/watch?v=X44CZTx0iMA&list=PLi2j5X2Nl1q9kYkp9ZHC-dJart3ZmotrV',
            'color': '#e0f2f1',
            'icon': 'format_quote'
        },
        {
            'name': 'sejarah_islam_general',
            'title': 'Sejarah Islam - General',
            'url': 'https://www.youtube.com/watch?v=IuKBAROKzXA&list=PLyQi9gHnMD5opxbtVOtNstiuqZ2wgvGCn',
            'color': '#f3e5f5',
            'icon': 'history_edu'
        },
        {
            'name': 'general_khutbah',
            'title': 'General (khutbah/Debat/Others)',
            'url': 'https://www.youtube.com/watch?v=EBlPihkQvhQ&list=PLaIm8KSGEyAFsj-6MaqmjlTdoTsWyjGz9',
            'color': '#fbe9e7',
            'icon': 'record_voice_over'
        }
    ]

    all_playlists_data = {}

    for playlist in playlists:
        print(f"Fetching videos from: {playlist['title']}")

        # Create directory for this playlist
        playlist_dir = os.path.join(ustaz_dir, playlist['name'])
        os.makedirs(playlist_dir, exist_ok=True)

        # Extract playlist ID from URL if it's a playlist URL
        url = playlist['url']
        
        # Check if URL contains a playlist ID
        if 'list=' in url:
            # It's a playlist URL - extract the playlist ID
            playlist_id = url.split('list=')[1].split('&')[0]  # Get the playlist ID part
            playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
        else:
            # It's a single video URL, use it as is
            playlist_url = url

        # Fetch videos using yt-dlp
        ydl_opts = {
            'extract_flat': True,
            'quiet': False,
            'skip_download': True,
            'playlist_end': None,  # No limit to videos - fetch all videos from playlist
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)

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

                # For single videos (not playlists), we need to handle differently
                elif playlist_info.get('_type') == 'video':
                    # This is a single video, not a playlist
                    video_info = {
                        'id': playlist_info['id'],
                        'title': playlist_info.get('title', 'Untitled'),
                        'url': f"https://www.youtube.com/watch?v={playlist_info['id']}",
                        'thumbnail': playlist_info.get('thumbnail', ''),
                        'duration': playlist_info.get('duration', 0),
                        'upload_date': playlist_info.get('upload_date', ''),
                        'view_count': playlist_info.get('view_count', 0)
                    }
                    videos.append(video_info)

                    # Save individual video info
                    video_file = os.path.join(playlist_dir, f"01_{playlist_info['id']}.json")
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
    <title>{playlist['title']} - Ustaz Salman</title>
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
            background: rgba(25, 118, 210, 0.05);
        }}

        .back-link:hover {{
            background: rgba(25, 118, 210, 0.1);
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
        <p>Ustaz Salman</p>
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
    print("Fetching Ustaz Salman's YouTube playlist videos...")
    print("=" * 60)

    try:
        data = fetch_salman_playlist_videos()
        print("\n" + "=" * 60)
        print("SUCCESSFULLY FETCHED SALMAN'S VIDEOS!")
        print("=" * 60)
        print("Directories created:")
        print("- ustaz/salman/kitab_seerah_nabawiyyah/")
        print("- ustaz/salman/empat_khalifah_rasul/")
        print("- ustaz/salman/pengenalan_uluhayah/")
        print("- ustaz/salman/hadis_40_imam_nawawi/")
        print("- ustaz/salman/sejarah_islam_general/")
        print("- ustaz/salman/general_khutbah/")

        print("\nEach directory contains:")
        print("- Individual video JSON files")
        print("- Playlist metadata JSON")
        print("- HTML page with embedded videos")
        print("\nTo view the videos, open any of the _embedded.html files in a browser.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()