#!/usr/bin/env python3
import os
import json
import subprocess
import sys
from pathlib import Path

def fetch_playlist_videos(playlist_url, playlist_name, directory):
    """Fetch videos from a YouTube playlist using yt-dlp"""
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Command to get playlist info with yt-dlp
    cmd = [
        'yt-dlp',
        '--flat-playlist',
        '--print-json',
        playlist_url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        playlist_data = json.loads(result.stdout)
        
        # Get individual video URLs from the playlist
        video_urls = []
        if isinstance(playlist_data, list):
            # If the output is a list of entries
            for entry in playlist_data:
                video_urls.append(f"https://www.youtube.com/watch?v={entry['id']}")
        else:
            # If it's a single entry, we still need to extract individual videos
            # Let's run yt-dlp again to get individual video info
            cmd = [
                'yt-dlp',
                '--flat-playlist',
                '--print-json',
                playlist_url
            ]
            # Execute command to get all videos in playlist
            result = subprocess.run(['yt-dlp', '--flat-playlist', '--print-json', playlist_url], 
                                  capture_output=True, text=True)
            
            # Process the output line by line (yt-dlp outputs one JSON per line for playlist entries)
            video_entries = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        video_entries.append(entry)
                    except json.JSONDecodeError:
                        continue

            # Extract video IDs
            video_ids = [entry['id'] for entry in video_entries if 'id' in entry]
            video_urls = [f"https://www.youtube.com/watch?v={vid_id}" for vid_id in video_ids]
        
        # Get detailed information for each video
        videos = []
        for i, video_url in enumerate(video_urls, 1):
            print(f"Processing video {i}/{len(video_urls)}: {video_url}")
            try:
                cmd = [
                    'yt-dlp',
                    '--print-json',
                    video_url
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                video_data = json.loads(result.stdout)
                
                video_info = {
                    "id": video_data['id'],
                    "title": video_data['title'],
                    "url": video_data['webpage_url'],
                    "thumbnail": video_data.get('thumbnail', ''),
                    "duration": video_data.get('duration', 0),
                    "upload_date": video_data.get('upload_date', ''),
                    "view_count": video_data.get('view_count', 0)
                }
                videos.append(video_info)
                
                # Save individual video file
                video_filename = f"{i:02d}_{video_data['id']}.json"
                video_path = os.path.join(directory, video_filename)
                with open(video_path, 'w', encoding='utf-8') as f:
                    json.dump(video_info, f, ensure_ascii=False, indent=2)
                    
            except subprocess.CalledProcessError as e:
                print(f"Error fetching video {video_url}: {e}")
                continue
            except json.JSONDecodeError as e:
                print(f"JSON decode error for video {video_url}: {e}")
                continue
        
        # Create metadata file
        metadata = {
            "name": playlist_name,
            "title": playlist_name,
            "url": playlist_url,
            "video_count": len(videos),
            "videos": videos
        }
        
        metadata_path = os.path.join(directory, f"{playlist_name.replace(' ', '_').replace('/', '_or_').lower()}_metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"Downloaded {len(videos)} videos to {directory}")
        return videos
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Error output: {e.stderr}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def create_html_embed_page(videos, playlist_name, output_dir):
    """Create an embedded HTML page with the videos in a grid format"""
    import math
    from datetime import timedelta

    # Calculate total duration
    total_duration_seconds = sum(video.get('duration', 0) for video in videos)
    total_duration = str(timedelta(seconds=total_duration_seconds))
    
    # Generate the HTML content
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{playlist_name} - Ustaz Halim</title>
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
            opacity: 0.9;
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-value {{
            font-size: 1.8rem;
            font-weight: 500;
        }}

        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.9;
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

        .video-duration {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            z-index: 10;
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
            <h1>{playlist_name}</h1>
            <p>A collection of teachings by Ustaz Halim</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{len(videos)}</div>
                    <div class="stat-label">Videos</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{total_duration}</div>
                    <div class="stat-label">Total Duration</div>
                </div>
            </div>
        </div>

        <a href="../../../index.html" class="back-link">
            <i class="material-icons" style="vertical-align: middle; font-size: 18px;">arrow_back</i>
            Back to Home
        </a>

        <div class="video-grid">'''
    
    for idx, video in enumerate(videos, 1):
        video_id = video['id']
        title = video['title']
        duration = str(timedelta(seconds=video.get('duration', 0)))
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
    html_filename = f"{playlist_name.replace(' ', '_').replace('/', '_or_').lower()}_embedded.html"
    html_path = os.path.join(output_dir, html_filename)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created HTML page with {len(videos)} videos")

def main():
    playlist_url = "https://www.youtube.com/watch?v=L6TBuMyg3v4&list=PLv_xoi4FGsu8-hzygSl6hOAZqPfc03UrU"
    playlist_name = "Kunci_Kunci_Rezeki_Menurut_Al_Quran_&_As_Sunnah"
    
    # Directory to save files
    directory = f"ustaz/halim/kunci_kunci_rezeki_menurut_al_quran_&_as_sunnah"
    
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Fetch videos
    videos = fetch_playlist_videos(playlist_url, playlist_name, directory)
    
    if videos:
        # Create HTML embed page
        create_html_embed_page(videos, playlist_name.replace('_', ' '), directory)
        print(f"Successfully processed {len(videos)} videos from the playlist")
    else:
        print("No videos were downloaded")

if __name__ == "__main__":
    main()