# Method for Creating Embedded Video Playlists for Ustaz

This document provides a comprehensive guide on how to add new YouTube playlists with embedded videos for Ustaz profiles in the system.

## Overview

The system generates embedded HTML pages with YouTube video grids for each Ustaz's playlists. This allows viewers to see all videos in a playlist on a single page with responsive embeds.

## Prerequisites

- Python 3.6+
- `yt-dlp` library installed
- Access to YouTube playlist URLs
- Basic understanding of the project structure

## Step-by-Step Process

### 1. Locate the Fetch Script

- Navigate to `/data/work/pmt/tools/`
- Identify the fetch script for the specific Ustaz (e.g., `fetch_qarni_videos.py`)

### 2. Identify Missing Playlists

- Check the main Ustaz HTML file (e.g., `qarni.html`) for playlist cards
- Identify which cards use `showVideos()` JavaScript function instead of direct links to embedded HTML files
- Find the playlist IDs used in the JavaScript mapping section

### 3. Get Playlist Information

- Locate the JavaScript playlist mapping in the Ustaz HTML file (typically around line 1047-1147)
- Extract playlist IDs, titles, and YouTube URLs
- Format the information to match the script's expected structure

### 4. Update the Fetch Script

- Open the appropriate fetch script (e.g., `fetch_qarni_videos.py`)
- Add new playlist entries to the `playlists` array
- Include the following information for each playlist:
  - `name`: snake_case identifier
  - `title`: Display title
  - `url`: Full YouTube playlist URL
  - `color`: Material Design color for the card
  - `icon`: Material Icons name

### 5. Run the Fetch Script

```bash
cd /data/work/pmt
python3 tools/fetch_qarni_videos.py
```

This will:
- Download all video metadata from YouTube playlists
- Create individual JSON files for each video
- Generate HTML embed pages with video grids
- Create metadata files for each playlist

### 6. Update HTML Links

- Open the main Ustaz HTML file (e.g., `qarni.html`)
- Find card elements that use `showVideos()` function
- Update these to link directly to embedded HTML files:
  ```html
  <!-- Before -->
  <div class="card" onclick="showVideos('playlist-id')">
  
  <!-- After -->
  <div class="card" onclick="window.location.href='ustaz/ustaz_name/playlist_name/playlist_name_embedded.html'">
  ```
- Ensure the directory and file names match the snake_case format from the script

### 7. Verify Implementation

- Check that all embedded HTML files were created in the respective directories
- Test that links from the main page direct to the embedded views
- Verify that all videos are properly displayed in the grid format
- Confirm video metadata (titles, durations, dates) is accurate

## File Structure Created

After running the script, the following structure is created:

```
ustaz/
└── ustaz_name/
    ├── playlist_name/
    │   ├── video_01.json
    │   ├── video_02.json
    │   ├── ...
    │   ├── playlist_name_embedded.html
    │   └── playlist_name_metadata.json
    ├── all_playlists.json
    └── index.html
```

## Tool Functions Used

### create_html_embed_page()
- Generates responsive HTML with YouTube embedded videos
- Creates grid layout with Material Design styling
- Includes video metadata and navigation features

### fetch_playlist_videos()
- Downloads playlist information using yt-dlp
- Extracts video metadata (ID, title, URL, duration, etc.)
- Handles pagination for large playlists

## Common Issues and Solutions

### Issue: Playlist not found or private
- Solution: Verify the YouTube playlist URL is correct and public
- Check if the playlist ID in the URL is valid

### Issue: Video embeds not showing
- Solution: Check that the YouTube video IDs are correctly extracted
- Ensure the embed URL format is correct: `https://www.youtube.com/embed/{video_id}`

### Issue: Card still using showVideos() function
- Solution: Update the HTML card to use direct link to embedded file
- Look for escaped quotes (`\"`) in the HTML that may affect string matching

## Best Practices

1. Always verify playlist URLs before adding them
2. Use consistent naming conventions (snake_case)
3. Choose appropriate Material Design colors and icons
4. Test all links after making changes
5. Verify all videos load properly in the embedded view
6. Keep the playlists array organized alphabetically if possible

## Future Implementation for New Ustaz

1. Create the ustaz directory pattern (e.g., `ustaz/ustaz_name/`)
2. Create a new fetch script for the ustaz if one doesn't exist
3. Add the ustaz to the main navigation/index files
4. Follow the same steps above to add their playlists

## Maintenance

- Periodically check that YouTube links remain active
- Update the scripts when new playlists are available
- Monitor for any changes to YouTube's API or URL structure