# AgentForge Browser Extension

Chrome extension companion for the AgentForge platform.

## Features
- **Summarize** — Extract and summarize page content
- **Translate** — Detect and translate page text  
- **Extract Text** — Extract readable text from the page

## Installation
1. Open `chrome://extensions/`
2. Enable **Developer mode**
3. Click **Load unpacked** → select this folder

## Structure
- `manifest.json` — Chrome extension config (MV3)
- `popup.html/js/css` — Popup UI
- `content.js` — Page text extraction
- `background.js` — API service worker