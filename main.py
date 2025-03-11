#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path
from utils.youtube import download_audio, extract_subtitles, get_video_metadata
from utils.transcribe import transcribe_audio
from utils.postprocess import improve_transcript
from utils.convert import convert_to_epub

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Download YouTube audio, transcribe, and improve readability")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", help="Output directory", default="./output")
    parser.add_argument("--fal-api-key", help="FAL.ai API key (optional if set as environment variable)")
    parser.add_argument("--gemini-api-key", help="Gemini API key (optional if set as environment variable)")
    args = parser.parse_args()
    
    # Set API keys
    if args.fal_api_key:
        os.environ["FAL_AI_API_KEY"] = args.fal_api_key
    if args.gemini_api_key:
        os.environ["GEMINI_API_KEY"] = args.gemini_api_key
    
    # Check for required API keys
    if not os.environ.get("FAL_AI_API_KEY"):
        print("Error: FAL_AI_API_KEY environment variable or --fal-api-key argument is required")
        return 1
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable or --gemini-api-key argument is required")
        return 1
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get video metadata
    try:
        print(f"Retrieving video metadata for {args.url}...")
        metadata = get_video_metadata(args.url)
        video_id = metadata.get("id", "video")
        video_title = metadata.get("title", f"YouTube Transcript {video_id}")
        video_creator = metadata.get("uploader", "Unknown Creator")
        print(f"Processing: {video_title} by {video_creator}")
    except Exception as e:
        print(f"Error retrieving metadata: {e}")
        return 1
    
    # Set up output paths
    output_base = output_dir / video_id
    raw_transcript_path = output_base.with_suffix(".raw.txt")
    md_path = output_base.with_suffix(".md")
    
    # Check for English subtitles
    print("Checking for existing subtitles...")
    subtitle_path = extract_subtitles(args.url, output_dir, video_id)
    
    transcript = None
    if subtitle_path:
        print(f"Using existing YouTube subtitles: {subtitle_path}")
        try:
            # The subtitle extraction already gives us clean text
            with open(subtitle_path, 'r', encoding='utf-8') as f:
                transcript = f.read()
        except Exception as e:
            print(f"Error reading subtitles: {e}")
            subtitle_path = None
    
    if not subtitle_path:
        # Download audio if no subtitles
        try:
            print("Downloading audio...")
            audio_path = download_audio(args.url, output_dir, video_id)
            print(f"Downloaded audio: {audio_path}")
            
            # Transcribe audio
            print("Transcribing audio (this may take a while)...")
            transcript = transcribe_audio(audio_path)
            print("Transcription completed")
            
            # Save raw transcript
            with open(raw_transcript_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
            print(f"Raw transcript saved to: {raw_transcript_path}")
        except Exception as e:
            print(f"Error during download or transcription: {e}")
            return 1
    
    if not transcript:
        print("Error: Failed to obtain transcript")
        return 1
    
    try:
        # Improve transcript with Gemini
        print("Improving transcript readability...")
        improved_transcript = improve_transcript(transcript)
        print("Transcript improvement completed")
        
        # Add metadata as a header
        md_content = f"# {video_title}\n\n"
        md_content += f"Creator: {video_creator}\n\n"
        md_content += f"Source: {args.url}\n\n"
        md_content += improved_transcript
        
        # Save as Markdown
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Markdown saved to: {md_path}")
        
        # Convert to EPUB
        print("Converting to EPUB...")
        epub_path = convert_to_epub(md_path, title=video_title, creator=video_creator)
        if epub_path:
            print(f"EPUB saved to: {epub_path}")
        else:
            print("EPUB conversion skipped or failed")
    except Exception as e:
        print(f"Error during post-processing: {e}")
        return 1
    
    print("\nProcessing complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
