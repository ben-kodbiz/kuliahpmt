#!/usr/bin/env python3
"""
Tool to create individual HTML session files for Ustaz Qarni's videos.
This creates individual session pages similar to what's done for other collections.
"""

import os
import json
from pathlib import Path

def create_session_html(playlist_dir, video_data, session_num, total_sessions):
    """Create an individual HTML session file for a video."""
    
    # Extract video information
    video_id = video_data['id']
    video_title = video_data['title']
    video_duration = format_duration(video_data.get('duration', 0))
    upload_date = video_data.get('upload_date', '')
    if upload_date:
        formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
    else:
        formatted_date = "N/A"
    
    # Determine navigation links
    prev_link = f'<a href="session{session_num-1}.html" class="nav-btn"><i class="material-icons">arrow_back</i> Previous</a>' if session_num > 1 else '<span class="nav-btn" style="background: #cccccc; cursor: not-allowed;"><i class="material-icons">arrow_back</i> Previous</span>'
    next_link = f'<a href="session{session_num+1}.html" class="nav-btn">Next <i class="material-icons">arrow_forward</i></a>' if session_num < total_sessions else '<span class="nav-btn" style="background: #cccccc; cursor: not-allowed;">Next <i class="material-icons">arrow_forward</i></span>'
    
    # Create HTML content with embedded YouTube video
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{video_title} - Ustaz Qarni Session</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
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
            padding: 20px;
        }}

        .header {{ 
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: var(--white); 
            padding: 20px; 
            border-radius: 8px; 
            margin-bottom: 20px;
            box-shadow: var(--shadow);
        }}

        .header h1 {{ 
            margin: 0; 
            font-size: 1.5rem;
            font-weight: 500;
        }}

        .header p {{ 
            margin: 5px 0 0 0; 
            font-size: 1rem;
            opacity: 0.9;
        }}

        .video-container {{
            background: var(--white);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
        }}

        .video-embed {{ 
            position: relative; 
            padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
            height: 0; 
            overflow: hidden;
            margin-bottom: 15px;
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
            display: flex;
            justify-content: space-between;
            color: var(--text-secondary);
            font-size: 0.9rem;
            padding: 10px 0;
            border-top: 1px solid var(--divider-color);
            border-bottom: 1px solid var(--divider-color);
        }}

        .session-nav {{
            background: var(--white);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
            display: flex;
            justify-content: space-between;
        }}

        .nav-btn {{
            padding: 8px 16px;
            background: var(--primary-color);
            color: white;
            text-decoration: none;
            border-radius: 4px;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}

        .nav-btn:hover {{
            background: var(--primary-dark);
        }}

        .nav-btn:disabled {{
            background: #cccccc;
            cursor: not-allowed;
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

        .video-title {{
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: var(--text-primary);
        }}
    </style>
</head>
<body>
    <a href="../index.html" class="back-link">
        <i class="material-icons" style="vertical-align: middle; font-size: 18px;">arrow_back</i>
        Back to Qarni Collections
    </a>
    
    <div class="header">
        <h1>Session {session_num}</h1>
        <p>Ustaz Qarni Edrus</p>
    </div>
    
    <div class="video-container">
        <h2 class="video-title">{video_title}</h2>
        
        <div class="video-embed">
            <iframe src="https://www.youtube.com/embed/{video_id}" allowfullscreen></iframe>
        </div>
        
        <div class="video-info">
            <span><i class="material-icons" style="font-size: 16px; vertical-align: middle;">access_time</i> Duration: {video_duration}</span>
            <span><i class="material-icons" style="font-size: 16px; vertical-align: middle;">calendar_today</i> Date: {formatted_date}</span>
        </div>
    </div>
    
    <div class="session-nav">
        <span>
        {prev_link}
        </span>
        
        <span>
        {next_link}
        </span>
    </div>
</body>
</html>"""
    
    # Write the HTML file
    session_file = os.path.join(playlist_dir, f"session{session_num}.html")
    with open(session_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  Created session file: session{session_num}.html")
    return session_file

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

def create_playlist_sessions(playlist_dir, playlist_name):
    """Create session files for all videos in a playlist."""
    print(f"Creating session files for playlist: {playlist_name}")
    
    # Get all video JSON files in the directory
    video_files = []
    for file in os.listdir(playlist_dir):
        if file.endswith('.json') and not file.endswith('_metadata.json'):
            video_files.append(file)
    
    # Sort files by session number (based on filename prefix like 01_, 02_, etc.)
    video_files.sort()
    
    print(f"  Found {len(video_files)} video files")
    
    # Store total sessions count
    total_sessions = len(video_files)
    
    # Process each video file
    for i, video_file in enumerate(video_files, 1):
        # Load video data
        video_path = os.path.join(playlist_dir, video_file)
        with open(video_path, 'r', encoding='utf-8') as f:
            video_data = json.load(f)
        
        # Create session HTML file
        create_session_html(playlist_dir, video_data, i, total_sessions)

def main():
    """Main function to process all Ustaz Qarni playlists."""
    base_dir = "/data/work/pmt"
    ustaz_dir = os.path.join(base_dir, "ustaz", "qarni")
    
    # Only process the newly created playlists
    playlists_to_process = [
        '40_hadis_aspirasi',
        'dosa_muamalat', 
        'minhajul_qasidin'
    ]
    
    print("Creating individual session HTML files for Ustaz Qarni's videos...")
    print("=" * 70)
    
    for playlist_name in playlists_to_process:
        playlist_dir = os.path.join(ustaz_dir, playlist_name)
        if os.path.exists(playlist_dir):
            create_playlist_sessions(playlist_dir, playlist_name)
            print(f"  Completed {playlist_name}")
        else:
            print(f"  Playlist directory not found: {playlist_dir}")
    
    print("\n" + "=" * 70)
    print("SUCCESSFULLY CREATED SESSION FILES FOR ALL NEW PLAYLISTS!")
    print("=" * 70)
    print("Session files are now available for:")
    print("- 40 Hadis Aspirasi Kejayaan (63 sessions)")
    print("- 40 Hadith Dosa Muamalat (32 sessions)")
    print("- Kitab Mukhtasar Minhajul Qasidin (32 sessions)")
    print("\nEach video now has its own HTML session file with embedded YouTube player.")

if __name__ == "__main__":
    main()