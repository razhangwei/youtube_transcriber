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
    clean_text = parse_vtt(vtt_path)
    
    # Save clean text
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(clean_text)
    
    return text_path

def parse_vtt(vtt_path):
    """Extract text from VTT subtitle file, removing timestamps and metadata"""
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove header
    content = re.sub(r'^WEBVTT\n.+\n\n', '', content, flags=re.DOTALL)
    
    # Extract text, ignore timestamps and speaker identifiers
    lines = []
    current_line = ""
    
    for line in content.split('\n'):
        # Skip timestamp lines or empty lines
        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', line) or not line.strip():
            if current_line:
                lines.append(current_line)
                current_line = ""
            continue
        
        # Skip VTT note lines
        if line.startswith('NOTE '):
            continue
        
        # Skip VTT identifier lines (typically just a number)
        if re.match(r'^\d+$', line.strip()):
            continue
            
        # Add text content
        if current_line:
            current_line += " " + line.strip()
        else:
            current_line = line.strip()
    
    # Don't forget the last line
    if current_line:
        lines.append(current_line)
    
    # Join lines into paragraphs with proper spacing
    paragraphs = []
    current_paragraph = ""
    
    for line in lines:
        # If this is a continuation of the same sentence or thought
        if not current_paragraph.endswith('.') and not current_paragraph.endswith('?') and not current_paragraph.endswith('!'):
            if current_paragraph:
                current_paragraph += " " + line
            else:
                current_paragraph = line
        else:
            # Start a new paragraph
            if current_paragraph:
                paragraphs.append(current_paragraph)
            current_paragraph = line
    
    # Add the last paragraph
    if current_paragraph:
        paragraphs.append(current_paragraph)
    
    return '\n\n'.join(paragraphs)
