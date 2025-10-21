# Tools Directory Structure and Linking

This document explains how the tools in the `/tools` directory are connected to and used by other parts of the application.

## Directory Structure

```
promedia-tajdid/
├── tools/                 # Contains all maintenance tools
│   ├── config.ini         # Universal configuration file
│   ├── search_*.py        # Various search tools
│   └── README.md          # Documentation for tools
├── scripts/               # Contains main application scripts
│   └── update_videos_ytdlp.py  # Main video update script
├── data/                  # Data output directory
└── *.html                 # Web application files
```

## Tool Connections

### 1. Main Update Script (`scripts/update_videos_ytdlp.py`)
- **Location**: `/scripts/update_videos_ytdlp.py`
- **Connected to**: `/tools/config.ini` (reads configuration)
- **Purpose**: Fetches latest videos for each ustaz and updates JSON files
- **Output Directory**: `/data/` (configured via config.ini)

### 2. Playlist Discovery Tools (`tools/search_*.py`)
- **Location**: `/tools/`
- **Connected to**: `/tools/config.ini` (reads/writes configuration)
- **Purpose**: Discover and verify YouTube playlists for content
- **Output Directory**: `/data/` (configured via config.ini)

## Configuration Flow

1. **All tools** read from `/tools/config.ini`
2. **Configuration values** determine:
   - Base directories
   - YouTube channel URLs
   - Search queries
   - Playlist minimum video counts
   - File extensions and naming conventions

3. **Output files** are written to `/data/` directory as configured

## GitHub Actions Integration

The GitHub workflow (`.github/workflows/update_videos.yml`) runs:
- `scripts/update_videos_ytdlp.py` which uses configuration from `tools/config.ini`

## Benefits of This Structure

1. **Centralized Configuration**: All settings in one place (`config.ini`)
2. **Easy Maintenance**: Change values in one file affects all tools
3. **Clear Separation**: Tools are separate from application scripts
4. **Scalable**: Easy to add new tools that follow the same pattern
5. **Documented**: README.md explains usage of each tool

## Adding New Tools

To add a new tool:
1. Place it in the `/tools/` directory
2. Have it read configuration from `/tools/config.ini`
3. Follow the same output directory pattern (`config.get('general', 'data_dir')`)
4. Document it in `/tools/README.md`