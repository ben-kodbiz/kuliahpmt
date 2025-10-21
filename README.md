# Promedia Tajdid - Ustaz Video Collections

This directory contains organized video collections from various ustaz (Islamic scholars) featured in the Promedia Tajdid application.

## Directory Structure

```
promedia-tajdid/
├── index.html                      # Main application
├── qarni.html                      # Ustaz Qarni Edrus page
├── fadzil.html                     # Ustaz Fadzil Kamaruddin page
├── halim.html                      # Ustaz Halim Hassan page
├── adli.html                       # Ustaz Adli Mohd Saad page
├── data/                           # JSON video data files
├── tools/                          # Utility scripts
│   ├── fetch_qarni_videos.py       # Fetch Qarni's video data
│   └── video_fetcher_config.ini    # Configuration file
├── ustaz/                          # Organized video collections
│   ├── index.html                  # Main ustaz collections page
│   └── qarni/                      # Ustaz Qarni Edrus collections
│       ├── index.html             # Qarni playlists navigation
│       ├── all_playlists.json     # Metadata for all playlists
│       ├── 1000_amalan_sunnah/     # "1000 Amalan Sunnah" playlist
│       │   ├── 01_*.json          # Individual video metadata
│       │   ├── 1000_amalan_sunnah_metadata.json
│       │   └── 1000_amalan_sunnah_embedded.html
│       ├── bacaan_pelik_ganjil/   # "Bacaan Pelik & Ganjil" playlist
│       │   ├── 01_*.json          # Individual video metadata
│       │   ├── bacaan_pelik_ganjil_metadata.json
│       │   └── bacaan_pelik_ganjil_embedded.html
│       └── 30_teknik_tadabbur/    # "30 Teknik Tepat Tadabbur" playlist
│           ├── 01_*.json          # Individual video metadata
│           ├── 30_teknik_tadabbur_metadata.json
│           └── 30_teknik_tadabbur_embedded.html
└── README.md                      # This file
```

## Completed Tasks

### 1. Ustaz Qarni Edrus Video Collection
- ✅ Fetched all videos from 3 authentic playlists:
  1. **1000 Amalan Sunnah Sehari-Hari** (32 videos)
  2. **Bacaan Pelik & Ganjil Dalam Solat Namun Sahih** (20 videos)
  3. **30 Teknik Tepat Tadabbur Al-Quran** (19 videos)
- ✅ Created individual JSON metadata files for each video
- ✅ Generated playlist metadata files
- ✅ Created HTML pages with embedded YouTube players
- ✅ Organized content in structured directory hierarchy

### 2. Navigation Pages
- ✅ Created main ustaz collections page (`ustaz/index.html`)
- ✅ Created Qarni-specific navigation page (`ustaz/qarni/index.html`)
- ✅ Updated main Qarni page to link to organized collections
- ✅ Created embedded video pages for each playlist

### 3. Tools
- ✅ Created `fetch_qarni_videos.py` tool to automate video fetching
- ✅ Organized videos in ustaz-specific directories
- ✅ Generated HTML embed pages with YouTube players

## How to View the Videos

1. **Navigate to `ustaz/qarni/index.html`** to see all playlists for Ustaz Qarni
2. **Click on any playlist card** to go to its embedded video page
3. **The embedded HTML pages** have YouTube players for each video
4. **Each video has metadata** including duration, upload date, and view count

## Authentic Playlists Included

### Ustaz Qarni Edrus (PROmediaTAJDID Channel)

1. **1000 Amalan Sunnah Sehari-Hari**
   - 32 videos from the official PROmediaTAJDID channel
   - URL: `https://www.youtube.com/playlist?list=PLv_xoi4FGsu8Y2CuKhUoRId0szziOz9He`

2. **Bacaan Pelik & Ganjil Dalam Solat Namun Sahih**
   - 20 videos from the official PROmediaTAJDID channel
   - URL: `https://www.youtube.com/playlist?list=PLv_xoi4FGsu_VrsuNVH8VqQVbxYLt22wc`

3. **30 Teknik Tepat Tadabbur Al-Quran**
   - 19 videos from the official PROmediaTAJDID channel
   - URL: `https://www.youtube.com/playlist?list=PLv_xoi4FGsu_OrjOhwUltHg927qCs5U-1`

## Video Data Format

Each individual video JSON file contains:
```json
{
  "id": "video_id",
  "title": "Video title",
  "url": "YouTube URL",
  "thumbnail": "Thumbnail URL",
  "duration": 3600,
  "upload_date": "YYYYMMDD",
  "view_count": 10000
}
```

## Playlist Metadata Format

Each playlist metadata file contains:
```json
{
  "name": "playlist_folder_name",
  "title": "Playlist title",
  "url": "YouTube playlist URL",
  "video_count": 32,
  "videos": [/* Array of video metadata */]
}
```

## Requirements

To run the tools, you need:
- Python 3.x
- yt-dlp library
- Internet connection

Install yt-dlp:
```bash
pip install yt-dlp
```

## Future Enhancements

Plans to expand the collection to include:
- Ustaz Fadzil Kamaruddin collections
- Ustaz Halim Hassan collections
- Ustaz Adli Mohd Saad collections

## Method for Adding New Playlists

To add new YouTube playlists with embedded videos for Ustaz, follow this process:

### Step-by-Step Process

#### 1. Locate the Fetch Script
- Navigate to `/data/work/pmt/tools/`
- Identify the fetch script for the specific Ustaz (e.g., `fetch_qarni_videos.py`)

#### 2. Identify Missing Playlists
- Check the main Ustaz HTML file (e.g., `qarni.html`) for playlist cards
- Identify which cards use `showVideos()` JavaScript function instead of direct links to embedded HTML files
- Find the playlist IDs used in the JavaScript mapping section

#### 3. Get Playlist Information
- Locate the JavaScript playlist mapping in the Ustaz HTML file (typically around line 1047-1147)
- Extract playlist IDs, titles, and YouTube URLs
- Format the information to match the script's expected structure

#### 4. Update the Fetch Script
- Open the appropriate fetch script (e.g., `fetch_qarni_videos.py`)
- Add new playlist entries to the `playlists` array
- Include the following information for each playlist:
  - `name`: snake_case identifier
  - `title`: Display title
  - `url`: Full YouTube playlist URL
  - `color`: Material Design color for the card
  - `icon`: Material Icons name

#### 5. Run the Fetch Script

```bash
cd /data/work/pmt
python3 tools/fetch_qarni_videos.py
```

This will:
- Download all video metadata from YouTube playlists
- Create individual JSON files for each video
- Generate HTML embed pages with video grids
- Create metadata files for each playlist

#### 6. Update HTML Links

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

#### 7. Verify Implementation
- Check that all embedded HTML files were created in the respective directories
- Test that links from the main page direct to the embedded views
- Verify that all videos are properly displayed in the grid format
- Confirm video metadata (titles, durations, dates) is accurate

### File Structure Created

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

### Tool Functions Used

#### create_html_embed_page()
- Generates responsive HTML with YouTube embedded videos
- Creates grid layout with Material Design styling
- Includes video metadata and navigation features

#### fetch_playlist_videos()
- Downloads playlist information using yt-dlp
- Extracts video metadata (ID, title, URL, duration, etc.)
- Handles pagination for large playlists

### Common Issues and Solutions

#### Issue: Playlist not found or private
- Solution: Verify the YouTube playlist URL is correct and public
- Check if the playlist ID in the URL is valid

#### Issue: Video embeds not showing
- Solution: Check that the YouTube video IDs are correctly extracted
- Ensure the embed URL format is correct: `https://www.youtube.com/embed/{video_id}`

#### Issue: Card still using showVideos() function
- Solution: Update the HTML card to use direct link to embedded file
- Look for escaped quotes (`\"`) in the HTML that may affect string matching

### Best Practices

1. Always verify playlist URLs before adding them
2. Use consistent naming conventions (snake_case)
3. Choose appropriate Material Design colors and icons
4. Test all links after making changes
5. Verify all videos load properly in the embedded view
6. Keep the playlists array organized alphabetically if possible

## License

All video content belongs to their respective owners (PROmediaTAJDID and other channels).
This repository provides tools to organize and access publicly available Islamic educational content.