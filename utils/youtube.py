import yt_dlp
import os
import re
from pathlib import Path

def get_video_metadata(url):
    """Get metadata for a YouTube video"""
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

def download_audio(url, output_dir, video_id):
    """Download audio from YouTube video"""
    output_path = Path(output_dir) / f"{video_id}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': str(output_path).replace('.mp3', ''),
        'quiet': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return output_path

def extract_subtitles(url, output_dir, video_id):
    """Extract English subtitles if available and convert to clean text"""
    output_dir = Path(output_dir)
    vtt_path = output_dir / f"{video_id}.en.vtt"
    text_path = output_dir / f"{video_id}.subtitles.txt"
    
    # First try to get manual subtitles
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': False,
        'subtitleslangs': ['en'],
        'outtmpl': str(output_dir / video_id),
        'quiet': True,
    }
    
    subtitles_found = False
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if ('requested_subtitles' in info_dict and 
            info_dict['requested_subtitles'] and 
            'en' in info_dict['requested_subtitles']):
            ydl.download([url])
            subtitles_found = True
    
    # If manual subtitles not found, try auto-generated ones
    if not subtitles_found:
        ydl_opts['writeautomaticsub'] = True
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if ('requested_subtitles' in info_dict and 
                info_dict['requested_subtitles'] and 
                'en' in info_dict['requested_subtitles']):
                ydl.download([url])
                subtitles_found = True
    
    if not subtitles_found or not vtt_path.exists():
        return None
    
    # Parse VTT to clean text
    try:
        clean_text = simple_vtt_parse(vtt_path)
        
        # Save clean text
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(clean_text)
        
        # Verify file was written successfully
        if os.path.getsize(text_path) == 0:
            print(f"Warning: Output file {text_path} is empty after writing")
            return None
            
        return text_path
    except Exception as e:
        print(f"Error parsing subtitles: {e}")
        return None

def simple_vtt_parse(vtt_path):
    """A simpler VTT parser as fallback"""
    try:
        with open(vtt_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Remove all HTML-like tags
        content = re.sub(r'<[^>]+>', '', content)
        
        # Remove all timestamp lines
        content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*', '', content)
        
        # Remove header
        content = re.sub(r'^WEBVTT.*\n', '', content)
        
        # Remove empty lines and get non-empty lines
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Remove duplicates while preserving order
        unique_lines = []
        seen = set()
        for line in lines:
            # Normalize line to avoid near-duplicates (lowercase, remove extra spaces)
            normalized = ' '.join(line.lower().split())
            if normalized not in seen:
                seen.add(normalized)
                unique_lines.append(line)
        
        return '\n'.join(unique_lines)
    except Exception as e:
        print(f"Error in simple_vtt_parse: {e}")
        return "Could not parse subtitles. Please manually check the VTT file."
