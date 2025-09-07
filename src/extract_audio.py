#!/usr/bin/env python3
"""
Audio Extractor - Extract audio from videos using ffmpeg and yt-dlp
"""

import os
import sys
import click
import yt_dlp
import ffmpeg
from pathlib import Path
from typing import Optional, List
import colorama
from colorama import Fore, Style

# Initialize colorama for Windows compatibility
colorama.init()

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
    
    def extract_from_local_file(self, input_file: str) -> bool:
        """Extract audio from a local video file"""
        input_path = Path(input_file)
        
        if not input_path.exists():
            click.echo(f"{Fore.RED}Error: File '{input_file}' not found{Style.RESET_ALL}")
            return False
        
        # Generate output filename
        output_filename = f"{input_path.stem}.{self.audio_format}"
        output_path = self.output_dir / output_filename
        
        click.echo(f"{Fore.CYAN}Extracting audio from: {input_file}{Style.RESET_ALL}")
        
        try:
            # Get quality settings
            settings = self.quality_settings.get(self.quality, self.quality_settings["high"])
            
            # Use ffmpeg to extract audio
            stream = ffmpeg.input(str(input_path))
            stream = ffmpeg.output(
                stream, 
                str(output_path),
                acodec='libmp3lame' if self.audio_format == 'mp3' else None,
                audio_bitrate=settings["bitrate"],
                ar=settings["sample_rate"]
            )
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
            click.echo(f"{Fore.GREEN}✓ Audio extracted to: {output_path}{Style.RESET_ALL}")
            return True
            
        except ffmpeg.Error as e:
            click.echo(f"{Fore.RED}FFmpeg error: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return False
    
    def extract_from_url(self, url: str) -> bool:
        """Download and extract audio from a URL using yt-dlp"""
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
@click.pass_context
def local(ctx, file_path):
    """Extract audio from a local video file"""
    extractor = ctx.obj['extractor']
    extractor.extract_from_local_file(file_path)

@cli.command()
@click.argument('video_url')
@click.pass_context
def url(ctx, video_url):
    """Download and extract audio from a URL"""
    extractor = ctx.obj['extractor']
    extractor.extract_from_url(video_url)

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
