# Audio Extractor

A Python tool for extracting audio from videos using ffmpeg and yt-dlp.

## Features

- Extract audio from local video files
- **Time range extraction with millisecond precision** - Extract specific segments with 1ms accuracy
- Download and extract audio from YouTube and other supported platforms
- Support for multiple audio formats (MP3, WAV, FLAC, AAC)
- Batch processing capabilities
- Command-line interface with flexible time format support
- **Comprehensive test suite** - 44+ tests covering all functionality

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
git clone https://github.com/stevenaubertin/audio-extractor.git
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

5. **Run tests to verify functionality** (Optional but recommended):
```bash
# Run core functionality tests (no dependencies required)
python run_tests.py

# Or run individual test suites
cd tests
python test_basic.py              # Core functionality tests
python test_millisecond_simple.py # Millisecond precision tests
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
# Extract entire audio
python src/extract_audio.py --format mp3 --quality high local "path/to/video.mp4"
```

### Extract audio from specific time ranges with millisecond precision:
```bash
# Extract from 1:30 to 2:45
python src/extract_audio.py --format mp3 local "video.mp4" --start-time 1:30 --end-time 2:45

# Extract 30 seconds starting from 1:00
python src/extract_audio.py --format mp3 local "video.mp4" --start-time 1:00 --duration 30

# Extract from 90.5 seconds for 2 minutes
python src/extract_audio.py --format wav local "video.mp4" --start-time 90.5 --duration 2:00

# Extract with millisecond precision
python src/extract_audio.py --format mp3 local "video.mp4" --start-time 1:23.456 --duration 30.250

# Extract precise segment with milliseconds
python src/extract_audio.py --format mp3 local "video.mp4" --start-time 00:01:23.750 --end-time 00:02:45.125

# Extract everything after 5 minutes
python src/extract_audio.py --format mp3 local "video.mp4" --start-time 5:00
```

**Time Format Options (all support millisecond precision):**
- `HH:MM:SS.mmm` - Hours, minutes, seconds, milliseconds (e.g., `01:23:45.678`)
- `MM:SS.mmm` - Minutes, seconds, milliseconds (e.g., `23:45.123`)
- `SS.mmm` - Seconds, milliseconds (e.g., `45.500`)
- Decimal seconds with up to 3 decimal places (e.g., `105.250`, `30.125`)

### Download and extract audio from a URL:
```bash
# Download entire audio
python src/extract_audio.py --format mp3 --quality high url "https://www.youtube.com/watch?v=VIDEO_ID"

# Download specific time range
python src/extract_audio.py --format mp3 url "https://www.youtube.com/watch?v=VIDEO_ID" --start-time 2:30 --duration 1:00

# Download with millisecond precision
python src/extract_audio.py --format mp3 url "https://www.youtube.com/watch?v=VIDEO_ID" --start-time 2:30.750 --duration 1:15.250
```

### Batch processing:
```bash
python src/extract_audio.py --format wav --quality medium batch "path/to/video_folder/"
```

### Check dependencies:
```bash
python src/extract_audio.py check-dependencies
```

### Run tests:
```bash
# Run all available tests
python run_tests.py

# Run specific test suites
cd tests
python test_basic.py              # Core tests (always work)
python test_millisecond_simple.py # Millisecond tests (always work)  
python test_audio_extractor.py    # Integration tests (requires dependencies)
```

## Options

### Global Options:
- `--format`: Audio format (mp3, wav, flac, aac) - default: mp3
- `--quality`: Audio quality (high, medium, low) - default: high
- `--output`: Output directory - default: ./output/

### Time Range Options (for `local` and `url` commands):
- `--start-time` / `-s`: Start time with millisecond precision (HH:MM:SS.mmm, MM:SS.mmm, or decimal seconds)
- `--duration` / `-d`: Duration from start time with millisecond precision (HH:MM:SS.mmm, MM:SS.mmm, or decimal seconds)  
- `--end-time` / `-e`: End time with millisecond precision (HH:MM:SS.mmm, MM:SS.mmm, or decimal seconds)

**Note**: Use either `--duration` OR `--end-time` with `--start-time`, not both.

## Time Range Extraction with Millisecond Precision

This tool supports precise time-based audio extraction with **millisecond accuracy**, similar to FFmpeg's time parameters:

### Supported Time Formats:
1. **HH:MM:SS.mmm** - Hours:Minutes:Seconds.Milliseconds (e.g., `01:23:45.678`)
2. **MM:SS.mmm** - Minutes:Seconds.Milliseconds (e.g., `23:45.123`)
3. **SS.mmm** - Seconds.Milliseconds (e.g., `45.500`)
4. **Decimal seconds** - Up to 3 decimal places for millisecond precision (e.g., `105.250`, `30.125`)

**Millisecond Support:**
- Milliseconds can be specified with 1-3 digits (e.g., `.5`, `.50`, `.500`)
- Values are automatically padded/interpreted correctly
- Maximum precision: 1 millisecond (0.001 seconds)
- All time parameters support millisecond precision

### Usage Patterns:

**Extract from start time to end time:**
```bash
python src/extract_audio.py --format mp3 local "video.mp4" --start-time 1:30 --end-time 3:45
```

**Extract duration from start time:**
```bash
python src/extract_audio.py --format mp3 local "video.mp4" --start-time 2:00 --duration 30
```

**Extract from start time to end of video:**
```bash
python src/extract_audio.py --format mp3 local "video.mp4" --start-time 5:00
```

**Millisecond precision examples:**
```bash
# Extract with sub-second precision
python src/extract_audio.py --format mp3 local "video.mp4" --start-time 1:23.456 --duration 30.750

# Extract precise segment for audio analysis
python src/extract_audio.py --format wav local "video.mp4" --start-time 00:01:23.125 --end-time 00:01:25.875

# Extract using decimal seconds with milliseconds
python src/extract_audio.py --format flac local "video.mp4" --start-time 83.250 --duration 12.500
```

### File Naming Convention:
Extracted files with time ranges are automatically named with time information:
- `video_130_to345.mp3` (from 1:30 to 3:45)
- `video_200_d30.mp3` (from 2:00 for 30 seconds)
- `video_50.mp3` (from 5:00 to end)
- `video_123456_d30250.mp3` (from 1:23.456 for 30.250 seconds with milliseconds)

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

## Testing

This project includes a comprehensive test suite to verify all functionality:

### Quick Testing (No Dependencies Required)
```bash
# Run all core tests
python run_tests.py

# Or run individual test files
cd tests
python test_basic.py              # 35 core functionality tests
python test_millisecond_simple.py # 9 millisecond precision tests
```

### Test Coverage
- ✅ **44/44 core tests passing**
- ✅ **Millisecond precision**: All time formats and edge cases
- ✅ **Input validation**: Error handling and parameter validation
- ✅ **Code structure**: Function availability and documentation
- ⚠️ **Integration tests**: Require dependencies (`pip install -r requirements.txt`)

### Test Organization
- `tests/test_basic.py` - Core functionality without external dependencies
- `tests/test_millisecond_simple.py` - Simple millisecond precision tests
- `tests/test_audio_extractor.py` - Full integration tests (requires deps)
- `tests/README.md` - Detailed testing documentation
- `run_tests.py` - Automated test runner

The core millisecond precision feature is **100% tested and working** without requiring any external dependencies.

## License

MIT License
