import os
import subprocess
from pathlib import Path

def convert_to_epub(md_path, title="YouTube Transcript", creator="Unknown"):
    """Convert Markdown to EPUB using Pandoc with metadata"""
    md_path = Path(md_path)
    epub_path = md_path.with_suffix('.epub')
    
    try:
        # Check if pandoc is installed
        result = subprocess.run(
            ["which", "pandoc"], 
            capture_output=True, 
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            print("Warning: Pandoc not found. Please install with 'brew install pandoc' on macOS.")
            return None
        
        # Add metadata
        metadata = [
            "--metadata", f"title={title}",
            "--metadata", f"creator={creator}",
            "--metadata", "lang=en-US"
        ]
        
        # Convert markdown to epub
        result = subprocess.run(
            ["pandoc", str(md_path), "-o", str(epub_path)] + metadata,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            print(f"Warning: EPUB conversion failed: {result.stderr}")
            return None
        
        return epub_path
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None
