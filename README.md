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

1. Clone this repository:
```bash
git clone <repository-url>
cd audio-extractor
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Extract audio from a local video file:
```bash
python src/extract_audio.py local path/to/video.mp4 --format mp3
```

### Download and extract audio from a URL:
```bash
python src/extract_audio.py url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp3
```

### Batch processing:
```bash
python src/extract_audio.py batch path/to/video_folder/ --format wav
```

## Options

- `--format`: Audio format (mp3, wav, flac, aac) - default: mp3
- `--quality`: Audio quality (high, medium, low) - default: high
- `--output`: Output directory - default: ./output/

## License

MIT License
