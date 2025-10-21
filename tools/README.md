# Tools Directory

This directory contains various tools used for maintaining and updating the Promedia Tajdid application.

## Tools Overview

### 1. search_official_ustaz_playlists.py
Searches the PROmediaTAJDID YouTube channel for official playlists for each ustaz.

**Usage:**
```bash
python search_official_ustaz_playlists.py
```

**Output:**
- Creates JSON files in the data directory with verified playlist information
- Generates individual files for each ustaz (e.g., `adli_official_playlists.json`)
- Generates a combined file with all results (`all_ustaz_official_playlists.json`)

### 2. search_playlists_by_keyword.py
Searches globally on YouTube for playlists using keywords.

**Usage:**
```bash
python search_playlists_by_keyword.py
```

**Output:**
- Creates JSON files with global search results
- Filters playlists with minimum video count (configured in config.ini)

### 3. search_all_ustaz_playlists.py
Searches for all ustaz (adli, halim, fadzil) playlists globally.

**Usage:**
```bash
python search_all_ustaz_playlists.py
```

**Output:**
- Creates JSON files with global playlist results for each ustaz
- Saves individual and combined results

### 4. search_qarni_playlists.py
Specifically searches for Ustaz Qarni playlists.

**Usage:**
```bash
python search_qarni_playlists.py
```

**Output:**
- Creates JSON files with Qarni playlist results

### 5. search_qarni_specific.py
Specific implementation for finding Qarni playlists with more than a certain number of videos.

**Usage:**
```bash
python search_qarni_specific.py
```

## Configuration

All tools use `config.ini` for configuration. This includes:

- Base directory paths
- YouTube channel URLs
- Search queries
- Minimum video counts
- File extensions

## Running the Tools

To run any tool, navigate to the tools directory and execute:

```bash
cd /path/to/promedia-tajdid/tools
python tool_name.py
```

## Dependencies

- Python 3.6+
- yt-dlp
- requests
- beautifulsoup4

Install dependencies with:
```bash
pip install yt-dlp requests beautifulsoup4
```