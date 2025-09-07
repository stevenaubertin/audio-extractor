#!/usr/bin/env python3
"""
Audio Extractor - Extract audio from videos using ffmpeg and yt-dlp
"""

import os
import sys
import re
import click
import yt_dlp
import ffmpeg
from pathlib import Path
from typing import Optional, List
import colorama
from colorama import Fore, Style

# Initialize colorama for Windows compatibility
colorama.init()

def parse_time_format(time_str: str) -> str:
    """Parse and validate time format with millisecond precision support
    
    Supported formats:
    - HH:MM:SS.mmm (e.g., 01:23:45.678)
    - MM:SS.mmm (e.g., 23:45.123)
    - SS.mmm (e.g., 45.500)
    - Decimal seconds (e.g., 105.250)
    
    Where:
    - HH: hours (0-99)
    - MM: minutes (0-59)
    - SS: seconds (0-59)
    - mmm: milliseconds (0-999, 1-3 digits)
    """
    if not time_str:
        raise click.BadParameter("Time parameter cannot be empty")
        
    # Remove whitespace
    time_str = time_str.strip()
    
    # Pattern for HH:MM:SS.mmm, MM:SS.mmm, or SS.mmm formats
    # Supports millisecond precision with 1-3 digits
    time_pattern = r'^(?:(?:([0-9]{1,2}):)?([0-5]?[0-9]):)?([0-5]?[0-9])(?:\.([0-9]{1,3}))?$'
    
    # Check if it's decimal seconds (integer or float with millisecond precision)
    if re.match(r'^\d+(?:\.\d{1,3})?$', time_str):
        return time_str
    
    # Check standard time format with optional milliseconds
    match = re.match(time_pattern, time_str)
    if match:
        hours, minutes, seconds, milliseconds = match.groups()
        
        # Validate milliseconds don't exceed 999
        if milliseconds and len(milliseconds) <= 3:
            ms_value = int(milliseconds.ljust(3, '0'))  # Pad to 3 digits
            if ms_value > 999:
                raise click.BadParameter(f"Invalid milliseconds: '{milliseconds}'. Must be 0-999")
        
        return time_str
    
    # If no match, raise an error with detailed format information
    raise click.BadParameter(
        f"Invalid time format: '{time_str}'. "
        "Supported formats:\n"
        "  • HH:MM:SS.mmm (e.g., 01:23:45.678)\n"
        "  • MM:SS.mmm (e.g., 23:45.123)\n"
        "  • SS.mmm (e.g., 45.500)\n"
        "  • Decimal seconds (e.g., 105.250)"
    )

def validate_time_range(start_time: Optional[str], duration: Optional[str], end_time: Optional[str]):
    """Validate time range parameters"""
    if duration and end_time:
        raise click.BadParameter("Cannot specify both --duration and --end-time. Use one or the other.")
    
    if (duration or end_time) and not start_time:
        raise click.BadParameter("--start-time is required when using --duration or --end-time")

class AudioExtractor:
    """Main class for audio extraction operations"""
    
    def __init__(self, output_dir: str = "output", audio_format: str = "mp3", quality: str = "high"):
        self.output_dir = Path(output_dir)
        self.audio_format = audio_format.lower()
        self.quality = quality
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
        
        # Quality settings
        self.quality_settings = {
            "high": {"bitrate": "320k", "sample_rate": "48000"},
            "medium": {"bitrate": "192k", "sample_rate": "44100"},
            "low": {"bitrate": "128k", "sample_rate": "44100"}
        }
    
    def extract_from_local_file(self, input_file: str, start_time: Optional[str] = None, duration: Optional[str] = None, end_time: Optional[str] = None) -> bool:
        """Extract audio from a local video file, optionally with time range"""
        input_path = Path(input_file)
        
        if not input_path.exists():
            click.echo(f"{Fore.RED}Error: File '{input_file}' not found{Style.RESET_ALL}")
            return False
        
        # Generate output filename with time range info if provided
        if start_time:
            time_info = f"_{start_time.replace(':', '')}"
            if duration:
                time_info += f"_d{duration.replace(':', '')}"
            elif end_time:
                time_info += f"_to{end_time.replace(':', '')}"
            output_filename = f"{input_path.stem}{time_info}.{self.audio_format}"
        else:
            output_filename = f"{input_path.stem}.{self.audio_format}"
            
        output_path = self.output_dir / output_filename
        
        # Display extraction info with time range if provided
        if start_time:
            time_info = f" from {start_time}"
            if duration:
                time_info += f" for {duration}"
            elif end_time:
                time_info += f" to {end_time}"
            click.echo(f"{Fore.CYAN}Extracting audio{time_info} from: {input_file}{Style.RESET_ALL}")
        else:
            click.echo(f"{Fore.CYAN}Extracting audio from: {input_file}{Style.RESET_ALL}")
        
        try:
            # Get quality settings
            settings = self.quality_settings.get(self.quality, self.quality_settings["high"])
            
            # Set up FFmpeg input with time parameters if provided
            input_args = {}
            if start_time:
                input_args['ss'] = start_time
                
            stream = ffmpeg.input(str(input_path), **input_args)
            
            # Set up output arguments
            output_args = {
                'acodec': 'libmp3lame' if self.audio_format == 'mp3' else None,
                'audio_bitrate': settings["bitrate"],
                'ar': settings["sample_rate"]
            }
            
            # Add duration or end time if provided
            if duration and not end_time:
                output_args['t'] = duration
            elif end_time and not duration:
                output_args['to'] = end_time
                
            stream = ffmpeg.output(stream, str(output_path), **output_args)
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
            click.echo(f"{Fore.GREEN}✓ Audio extracted to: {output_path}{Style.RESET_ALL}")
            return True
            
        except ffmpeg.Error as e:
            click.echo(f"{Fore.RED}FFmpeg error: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return False
    
    def extract_from_url(self, url: str, start_time: Optional[str] = None, duration: Optional[str] = None, end_time: Optional[str] = None) -> bool:
        """Download and extract audio from a URL using yt-dlp, optionally with time range"""
        # Display download info with time range if provided
        if start_time:
            time_info = f" from {start_time}"
            if duration:
                time_info += f" for {duration}"
            elif end_time:
                time_info += f" to {end_time}"
            click.echo(f"{Fore.CYAN}Downloading and extracting audio{time_info} from: {url}{Style.RESET_ALL}")
        else:
            click.echo(f"{Fore.CYAN}Downloading and extracting audio from: {url}{Style.RESET_ALL}")
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.audio_format,
                'preferredquality': self.quality_settings[self.quality]["bitrate"].replace('k', ''),
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        # Add time range options for yt-dlp if provided
        if start_time:
            # Calculate end time in seconds if we have duration
            if duration:
                # Convert times to seconds for calculation
                start_seconds = self._time_to_seconds(start_time)
                duration_seconds = self._time_to_seconds(duration)
                end_seconds = start_seconds + duration_seconds
                ydl_opts['download_ranges'] = [{'start_time': start_seconds, 'end_time': end_seconds}]
            elif end_time:
                start_seconds = self._time_to_seconds(start_time)
                end_seconds = self._time_to_seconds(end_time)
                ydl_opts['download_ranges'] = [{'start_time': start_seconds, 'end_time': end_seconds}]
            else:
                # Only start time provided
                start_seconds = self._time_to_seconds(start_time)
                ydl_opts['download_ranges'] = [{'start_time': start_seconds}]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            click.echo(f"{Fore.GREEN}✓ Audio downloaded and extracted to: {self.output_dir}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            click.echo(f"{Fore.RED}Error downloading from URL: {e}{Style.RESET_ALL}")
            return False
    
    def batch_extract_local(self, input_dir: str) -> List[str]:
        """Extract audio from all video files in a directory"""
        input_path = Path(input_dir)
        
        if not input_path.is_dir():
            click.echo(f"{Fore.RED}Error: '{input_dir}' is not a directory{Style.RESET_ALL}")
            return []
        
        # Common video file extensions
        video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
        video_files = [f for f in input_path.iterdir() if f.suffix.lower() in video_extensions]
        
        if not video_files:
            click.echo(f"{Fore.YELLOW}No video files found in '{input_dir}'{Style.RESET_ALL}")
            return []
        
        click.echo(f"{Fore.CYAN}Found {len(video_files)} video file(s) for processing{Style.RESET_ALL}")
        
        successful_extractions = []
        failed_extractions = []
        
        for video_file in video_files:
            click.echo(f"{Fore.BLUE}Processing: {video_file.name}{Style.RESET_ALL}")
            
            if self.extract_from_local_file(str(video_file)):
                successful_extractions.append(str(video_file))
            else:
                failed_extractions.append(str(video_file))
        
        # Summary
        click.echo(f"\n{Fore.GREEN}Batch processing completed:{Style.RESET_ALL}")
        click.echo(f"  ✓ Successful: {len(successful_extractions)}")
        click.echo(f"  ✗ Failed: {len(failed_extractions)}")
        
        if failed_extractions:
            click.echo(f"\n{Fore.RED}Failed files:{Style.RESET_ALL}")
            for failed_file in failed_extractions:
                click.echo(f"  - {failed_file}")
        
        return successful_extractions
    
    def _time_to_seconds(self, time_str: str) -> float:
        """Convert time string to seconds"""
        if not time_str:
            return 0
            
        # If it's already in seconds (float or int)
        if re.match(r'^\d+(?:\.\d+)?$', time_str):
            return float(time_str)
            
        # Parse HH:MM:SS, MM:SS format
        parts = time_str.split(':')
        if len(parts) == 3:  # HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:  # MM:SS
            return int(parts[0]) * 60 + float(parts[1])
        else:
            return float(time_str)

@click.group()
@click.option('--format', default='mp3', 
              type=click.Choice(['mp3', 'wav', 'flac', 'aac']), 
              help='Audio format')
@click.option('--quality', default='high', 
              type=click.Choice(['high', 'medium', 'low']), 
              help='Audio quality')
@click.option('--output', default='output', 
              help='Output directory')
@click.pass_context
def cli(ctx, format, quality, output):
    """Audio Extractor - Extract audio from videos using ffmpeg and yt-dlp"""
    ctx.ensure_object(dict)
    ctx.obj['extractor'] = AudioExtractor(output, format, quality)
    
    # Display configuration
    click.echo(f"{Fore.MAGENTA}Audio Extractor Configuration:{Style.RESET_ALL}")
    click.echo(f"  Format: {format}")
    click.echo(f"  Quality: {quality}")
    click.echo(f"  Output Directory: {output}")
    click.echo()

@cli.command()
@click.argument('file_path')
@click.option('--start-time', '-s', help='Start time (HH:MM:SS.mmm, MM:SS.mmm, or seconds with millisecond precision)')
@click.option('--duration', '-d', help='Duration (HH:MM:SS.mmm, MM:SS.mmm, or seconds with millisecond precision)')
@click.option('--end-time', '-e', help='End time (HH:MM:SS.mmm, MM:SS.mmm, or seconds with millisecond precision)')
@click.pass_context
def local(ctx, file_path, start_time, duration, end_time):
    """Extract audio from a local video file with millisecond precision
    
    Time formats supported (all with optional millisecond precision):
    - HH:MM:SS.mmm (e.g., 01:23:45.678)
    - MM:SS.mmm (e.g., 23:45.123)
    - Decimal seconds (e.g., 105.250)
    
    Examples:
    - Extract from 1:30 to 2:45: --start-time 1:30 --end-time 2:45
    - Extract 30 seconds from 1:00: --start-time 1:00 --duration 30
    - Extract from 90.5 seconds for 2 minutes: --start-time 90.5 --duration 2:00
    - Extract with millisecond precision: --start-time 1:23.456 --duration 30.250
    - Extract precise segment: --start-time 00:01:23.750 --end-time 00:02:45.125
    """
    # Validate and parse time parameters
    try:
        if start_time:
            start_time = parse_time_format(start_time)
        if duration:
            duration = parse_time_format(duration)
        if end_time:
            end_time = parse_time_format(end_time)
            
        validate_time_range(start_time, duration, end_time)
        
    except click.BadParameter as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return
    
    extractor = ctx.obj['extractor']
    extractor.extract_from_local_file(file_path, start_time, duration, end_time)

@cli.command()
@click.argument('video_url')
@click.option('--start-time', '-s', help='Start time (HH:MM:SS.mmm, MM:SS.mmm, or seconds with millisecond precision)')
@click.option('--duration', '-d', help='Duration (HH:MM:SS.mmm, MM:SS.mmm, or seconds with millisecond precision)')
@click.option('--end-time', '-e', help='End time (HH:MM:SS.mmm, MM:SS.mmm, or seconds with millisecond precision)')
@click.pass_context
def url(ctx, video_url, start_time, duration, end_time):
    """Download and extract audio from a URL with millisecond precision
    
    Time formats supported (all with optional millisecond precision):
    - HH:MM:SS.mmm (e.g., 01:23:45.678)
    - MM:SS.mmm (e.g., 23:45.123)
    - Decimal seconds (e.g., 105.250)
    
    Examples:
    - Extract from 1:30 to 2:45: --start-time 1:30 --end-time 2:45
    - Extract 30 seconds from 1:00: --start-time 1:00 --duration 30
    - Extract with millisecond precision: --start-time 1:23.456 --duration 30.250
    """
    # Validate and parse time parameters
    try:
        if start_time:
            start_time = parse_time_format(start_time)
        if duration:
            duration = parse_time_format(duration)
        if end_time:
            end_time = parse_time_format(end_time)
            
        validate_time_range(start_time, duration, end_time)
        
    except click.BadParameter as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return
    
    extractor = ctx.obj['extractor']
    extractor.extract_from_url(video_url, start_time, duration, end_time)

@cli.command()
@click.argument('directory_path')
@click.pass_context
def batch(ctx, directory_path):
    """Batch extract audio from all videos in a directory"""
    extractor = ctx.obj['extractor']
    extractor.batch_extract_local(directory_path)

@cli.command()
def check_dependencies():
    """Check if required dependencies are available"""
    click.echo(f"{Fore.CYAN}Checking dependencies...{Style.RESET_ALL}")
    
    # Check FFmpeg
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            click.echo(f"{Fore.GREEN}✓ FFmpeg is installed{Style.RESET_ALL}")
        else:
            click.echo(f"{Fore.RED}✗ FFmpeg check failed{Style.RESET_ALL}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        click.echo(f"{Fore.RED}✗ FFmpeg not found in PATH{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}  Please install FFmpeg: https://ffmpeg.org/download.html{Style.RESET_ALL}")
    
    # Check Python packages
    try:
        import yt_dlp
        click.echo(f"{Fore.GREEN}✓ yt-dlp is installed{Style.RESET_ALL}")
    except ImportError:
        click.echo(f"{Fore.RED}✗ yt-dlp not installed{Style.RESET_ALL}")
    
    try:
        import ffmpeg
        click.echo(f"{Fore.GREEN}✓ ffmpeg-python is installed{Style.RESET_ALL}")
    except ImportError:
        click.echo(f"{Fore.RED}✗ ffmpeg-python not installed{Style.RESET_ALL}")

if __name__ == '__main__':
    cli()
