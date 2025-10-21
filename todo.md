# TODO.md - Promedia Tajdid Automation Plan

### Stage 0: Init
- [ ] Ensure repo cloned locally or initialized on GitHub.
- [ ] Verify `.github/workflows/update_videos.yml` exists.
- [ ] Check that `yt-dlp` is available in workflow runners.

### Stage 1: Static Frontend Setup
- [ ] Deploy base HTML pages (index.html, ustaz pages).
- [ ] Confirm links between preacher pages work correctly.

### Stage 2: JSON Data Integration
- [ ] Run `scripts/update_videos_ytdlp.py` manually to generate `/data/*.json`.
- [ ] Verify frontend loads JSON video list dynamically.

### Stage 3: GitHub Workflow Test
- [ ] Manually trigger the workflow via GitHub Actions tab.
- [ ] Ensure it fetches new videos and commits updated JSON.

### Stage 4: Schedule Automation
- [ ] Validate that cron trigger (`0 6 * * *`) runs daily.
- [ ] Check commit history to confirm automation works.

### Stage 5: Deployment
- [ ] Enable GitHub Pages or Netlify to host static site.
- [ ] Verify videos update without redeployment.

### Stage 6: Optimization (optional)
- [ ] Add caching or filtering to JS loader.
- [ ] Add thumbnails or search filters for each preacher.
