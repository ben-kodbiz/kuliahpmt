#!/usr/bin/env python3
import os
import json
import subprocess
from datetime import timedelta

def seconds_to_hms(seconds):
    duration = timedelta(seconds=seconds)
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):01d}:{int(minutes):02d}:{int(seconds):02d}"

def format_duration(seconds):
    duration = timedelta(seconds=seconds)
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours >= 1:
        return f"{int(hours)}h {int(minutes)}m"
    elif minutes >= 1:
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        return f"{int(seconds)}s"

def format_total_duration(total_seconds):
    duration = timedelta(total_seconds)
    days, remainder = divmod(duration.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days:
        parts.append(f"{int(days)}d")
    if hours:
        parts.append(f"{int(hours)}h")
    if minutes:
        parts.append(f"{int(minutes)}m")
    if seconds:
        parts.append(f"{int(seconds)}s")
    
    return " ".join(parts) if parts else "0s"

def create_html_embed_page(videos, playlist_name, output_dir):
    """Create an embedded HTML page with the videos in a grid format"""
    
    # Calculate total duration
    total_duration_seconds = sum(video.get('duration', 0) for video in videos)
    total_duration = format_total_duration(total_duration_seconds)
    
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

def fetch_and_process_playlist():
    playlist_url = "https://www.youtube.com/watch?v=4EB3jZ52BvA&list=PLv_xoi4FGsu9uIvdnUZd7KI2U3PBvcBAp"
    playlist_name = "40_Cara_Merubah_Masalah_Menjadi_Anugerah"
    
    # Directory to save files
    directory = f"ustaz/halim/40_cara_merubah_masalah_menjadi_anugerah"
    
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Get video data using yt-dlp
    result = subprocess.run([
        'yt-dlp',
        '--flat-playlist',
        '--print-json',
        playlist_url
    ], capture_output=True, text=True)
    
    # Process the output line by line (yt-dlp outputs one JSON per line for playlist entries)
    video_entries = []
    for line in result.stdout.strip().split('\n'):
        if line.strip():
            try:
                entry = json.loads(line)
                if entry.get('_type') == 'url':  # It's a video entry
                    video_entries.append(entry)
            except json.JSONDecodeError:
                continue
    
    # Convert video entries to the format we need and save individual files
    videos = []
    for i, entry in enumerate(video_entries, 1):
        video_info = {
            "id": entry['id'],
            "title": entry['title'],
            "url": entry['webpage_url'],
            "thumbnail": entry.get('thumbnails', [{}])[0].get('url', '') if entry.get('thumbnails') else '',
            "duration": entry.get('duration', 0),
            "upload_date": entry.get('upload_date', ''),
            "view_count": entry.get('view_count', 0)
        }
        videos.append(video_info)
        
        # Save individual video file
        video_filename = f"{i:02d}_{entry['id']}.json"
        video_path = os.path.join(directory, video_filename)
        with open(video_path, 'w', encoding='utf-8') as f:
            json.dump(video_info, f, ensure_ascii=False, indent=2)
    
    # Create metadata file
    metadata = {
        "name": playlist_name.replace('_', ' '),
        "title": playlist_name.replace('_', ' '),
        "url": playlist_url,
        "video_count": len(videos),
        "videos": videos
    }
    
    metadata_path = os.path.join(directory, f"{playlist_name.lower()}_metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    # Create HTML embed page
    if videos:
        create_html_embed_page(videos, playlist_name.replace('_', ' '), directory)
        print(f"Successfully processed {len(videos)} videos from the playlist")
        
        # Return the data needed for integration
        # Get first video thumbnail for the card
        first_video = videos[0] if videos else {}
        first_thumbnail = first_video.get('thumbnail', '')
        
        return {
            'name': playlist_name.replace('_', ' '),
            'directory': directory,
            'video_count': len(videos),
            'first_thumbnail': first_thumbnail,
            'videos': videos
        }
    
    return None

if __name__ == "__main__":
    result = fetch_and_process_playlist()
    if result:
        print(f"Playlist '{result['name']}' has been created successfully in {result['directory']} with {result['video_count']} videos.")
    else:
        print("Failed to process the playlist")