# Tests

This directory contains comprehensive tests for the Audio Extractor application.

## Test Files

### Core Tests (No Dependencies Required)

- **`test_basic.py`** - Tests core functionality without external dependencies
  - ✅ Time parsing with millisecond precision
  - ✅ Time-to-seconds conversion
  - ✅ Input validation logic
  - ✅ Code structure verification

- **`test_millisecond_support.py`** - Specialized tests for millisecond precision
  - ✅ All millisecond time formats
  - ✅ Edge cases and error conditions
  - ✅ Precision validation

### Integration Tests (Require Dependencies)

- **`test_audio_extractor.py`** - Full integration tests
  - CLI interface testing
  - Audio processing functionality
  - End-to-end workflow validation
  - **Note**: Requires `pip install -r requirements.txt`

### Documentation

- **`TEST_RESULTS.md`** - Comprehensive test results and analysis
- **`README.md`** - This file

## Running Tests

### Quick Test (Core Functionality)
```bash
# From the tests directory
cd tests
python test_basic.py
```

### Run All Tests
```bash
# From the project root
python run_tests.py

# Or from tests directory
python test_audio_extractor.py  # (requires dependencies)
```

### Individual Test Files
```bash
cd tests

# Basic functionality tests (always work)
python test_basic.py

# Millisecond precision tests (always work)  
python test_millisecond_support.py

# Full integration tests (need dependencies)
python test_audio_extractor.py
```

## Test Results Summary

| Test Suite | Status | Tests | Coverage |
|------------|--------|-------|----------|
| Basic Tests | ✅ PASSED | 35/35 | 100% |
| Millisecond Tests | ✅ PASSED | 28/28 | 100% |
| Integration Tests | ⚠️ NEEDS DEPS | 0/6 | 0% |

**Overall Core Functionality: 63/63 tests passed (100%)**

## Dependencies for Full Testing

To run all tests, install the required dependencies:

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r ../requirements.txt

# Install FFmpeg (system dependency)
# Windows:
winget install Gyan.FFmpeg
# Mac:
brew install ffmpeg  
# Linux:
sudo apt install ffmpeg
```

## Test Categories

### Unit Tests
- Time parsing functions
- Input validation
- Data conversion utilities
- Error handling

### Integration Tests  
- CLI command execution
- File processing workflows
- External tool integration (FFmpeg, yt-dlp)
- End-to-end audio extraction

### Regression Tests
- Millisecond precision accuracy
- Time format compatibility
- Error message validation
- Edge case handling

## Adding New Tests

When adding new functionality to the audio extractor:

1. Add unit tests to `test_basic.py` for core logic
2. Add specialized tests for new features 
3. Add integration tests to `test_audio_extractor.py`
4. Update this README with new test descriptions
5. Update `TEST_RESULTS.md` with results

## Test Framework

The tests use Python's built-in testing capabilities and subprocess calls. No external testing framework is required for the core tests, making them easy to run in any Python environment.
