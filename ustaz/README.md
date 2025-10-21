# Ustaz Video Collection Tools

This directory contains tools and organized collections of videos from various ustaz (Islamic scholars) featured in the Promedia Tajdid application.

## Directory Structure

```
ustaz/
├── index.html                          # Main navigation page for all ustaz collections
├── qarni/                              # Ustaz Qarni Edrus collections
│   ├── index.html                      # Navigation page for Qarni's playlists
│   ├── all_playlists.json              # Metadata for all of Qarni's playlists
│   ├── 1000_amalan_sunnah/             # "1000 Amalan Sunnah Sehari-Hari" playlist
│   │   ├── 01_*.json                   # Individual video metadata files
│   │   ├── 1000_amalan_sunnah_metadata.json  # Playlist metadata
│   │   └── 1000_amalan_sunnah_embedded.html  # Embedded YouTube player
│   ├── bacaan_pelik_ganjil/            # "Bacaan Pelik & Ganjil" playlist
│   │   ├── 01_*.json                   # Individual video metadata files
│   │   ├── bacaan_pelik_ganjil_metadata.json
│   │   └── bacaan_pelik_ganjil_embedded.html
│   └── 30_teknik_tadabbur/             # "30 Teknik Tepat Tadabbur Al-Quran" playlist
│       ├── 01_*.json                   # Individual video metadata files
│       ├── 30_teknik_tadabbur_metadata.json
│       └── 30_teknik_tadabbur_embedded.html
├── fadzil/                             # Coming soon: Ustaz Fadzil Kamaruddin collections
├── halim/                              # Coming soon: Ustaz Halim Hassan collections
└── adli/                               # Coming soon: Ustaz Adli Mohd Saad collections
```

## Available Tools

### 1. fetch_qarni_videos.py
Fetches video data from Ustaz Qarni Edrus's authentic YouTube playlists.

**Usage:**
```bash
cd tools
python fetch_qarni_videos.py
```

**Features:**
- Fetches videos from all 3 authentic Qarni playlists
- Creates individual JSON metadata files for each video
- Generates playlist metadata files
- Creates HTML pages with embedded YouTube players
- Organizes content in a structured directory hierarchy

## How to View the Videos

1. Navigate to `ustaz/qarni/index.html` to see all playlists for Ustaz Qarni
2. Click on any playlist card to go to its embedded video page
3. The embedded HTML pages have YouTube players for each video
4. Each video has metadata including duration, upload date, and view count

## Authentic Playlists Included

### Ustaz Qarni Edrus

1. **1000 Amalan Sunnah Sehari-Hari**
   - 32 videos from the official PROmediaTAJDID channel
   - URL: `https://www.youtube.com/playlist?list=PLv_xoi4FGsu8Y2CuKhUoRId0szziOz9He`

2. **Bacaan Pelik & Ganjil Dalam Solat Namun Sahih**
   - 20 videos from the official PROmediaTAJDID channel
   - URL: `https://www.youtube.com/playlist?list=PLv_xoi4FGsu_VrsuNVH8VqQVbxYLt22wc`

3. **30 Teknik Tepat Tadabbur Al-Quran**
   - 19 videos from the official PROmediaTAJDID channel
   - URL: `https://www.youtube.com/playlist?list=PLv_xoi4FGsu_OrjOhwUltHg927qCs5U-1`

## Tools Directory

The `tools/` directory contains utilities for managing and updating video collections:

- `fetch_qarni_videos.py` - Fetches Qarni's video data
- `video_fetcher_config.ini` - Configuration file for all tools

## Future Enhancements

Plans to expand the collection to include:
- Ustaz Fadzil Kamaruddin collections
- Ustaz Halim Hassan collections
- Ustaz Adli Mohd Saad collections

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

## License

All video content belongs to their respective owners (PROmediaTAJDID and other channels).
This repository provides tools to organize and access publicly available Islamic educational content.