# Audio Extractor

A Python tool for extracting audio from videos using ffmpeg and yt-dlp.

## Features

- Extract audio from local video files
- Download and extract audio from YouTube and other supported platforms
- Support for multiple audio formats (MP3, WAV, FLAC, AAC)
- Batch processing capabilities
- Command-line interface

## Prerequisites

- Python 3.8 or higher
- FFmpeg installed and available in PATH

### Installing FFmpeg

**Windows:**
```bash
# Using chocolatey
choco install ffmpeg

# Using winget
winget install Gyan.FFmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## Installation

> ⚠️ **Important**: It is **strongly recommended** to use a virtual environment to avoid conflicts with system packages and ensure proper dependency management.

1. Clone this repository:
```bash
git clone <repository-url>
cd audio-extractor
```

2. **Create and activate a virtual environment** (Recommended):

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Verify installation:
```bash
python src/extract_audio.py check-dependencies
```

### Virtual Environment Management

**To deactivate the virtual environment:**
```bash
deactivate
```

**To reactivate later:**
```powershell
# Windows
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

## Quick Start

After installation, test the tool with a video file:

```bash
# Extract audio as MP3 (high quality)
python src/extract_audio.py --format mp3 --quality high local "your_video.mp4"

# The extracted audio will be saved to the output/ directory
```

## Usage

> 💡 **Note**: Make sure your virtual environment is activated before running any commands (you should see `(venv)` in your terminal prompt).

### Extract audio from a local video file:
```bash
python src/extract_audio.py --format mp3 --quality high local "path/to/video.mp4"
```

### Download and extract audio from a URL:
```bash
python src/extract_audio.py --format mp3 --quality high url "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Batch processing:
```bash
python src/extract_audio.py --format wav --quality medium batch "path/to/video_folder/"
```

### Check dependencies:
```bash
python src/extract_audio.py check-dependencies
```

## Options

- `--format`: Audio format (mp3, wav, flac, aac) - default: mp3
- `--quality`: Audio quality (high, medium, low) - default: high
- `--output`: Output directory - default: ./output/

## Troubleshooting

### Virtual Environment Issues

**If you get "execution policy" errors on Windows:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**If the virtual environment activation doesn't work:**
- Make sure you're in the project directory
- Try using the full path: `.\venv\Scripts\Activate.ps1`
- On some systems, you might need: `python -m venv --copies venv`

**If packages aren't found after activation:**
- Verify the virtual environment is active (look for `(venv)` in your prompt)
- Try: `python -m pip list` to see installed packages
- Reinstall requirements: `pip install -r requirements.txt`

### FFmpeg Issues

**If FFmpeg is not found:**
- Ensure FFmpeg is installed and in your system PATH
- Test with: `ffmpeg -version`
- Restart your terminal after installing FFmpeg

## License

MIT License
