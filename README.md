# YouTube Transcription Tool

A comprehensive tool to download YouTube audio, transcribe it, and improve readability with AI.

## Features

- Download audio from YouTube videos
- Extract existing English subtitles when available
- Transcribe audio using the Wizper API (large v3 model)
- Post-process transcripts with Gemini AI to improve readability
- Output both Markdown and EPUB formats

## Requirements

- Python 3.7+
- API keys:
  - FAL.ai (for Wizper transcription)
  - Google (for Gemini post-processing)
- Pandoc (for EPUB conversion)

### Installing Pandoc

On macOS:
```
brew install pandoc
```

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd youtube_transcriber
```

2. Create a virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up API keys:
```
export FAL_AI_API_KEY="your-fal-ai-key"
export GEMINI_API_KEY="your-gemini-key"
```

## Usage

Basic usage:
```
python main.py https://www.youtube.com/watch?v=XXXXXXXXXXX
```

With custom output directory:
```
python main.py https://www.youtube.com/watch?v=XXXXXXXXXXX -o /path/to/output
```

Providing API keys via command line:
```
python main.py https://www.youtube.com/watch?v=XXXXXXXXXXX --fal-api-key YOUR_KEY --gemini-api-key YOUR_KEY
```

## How It Works

1. The script first checks if the YouTube video has existing English subtitles
2. If subtitles exist, it uses them directly; otherwise, it downloads the audio and transcribes it
3. The transcript is then post-processed with Gemini AI to:
   - Improve paragraphing
   - Format lists properly
   - Remove filler words
   - Enhance sentence structure
   - Emphasize key information
   - Add annotations for non-verbal cues
4. The improved transcript is saved as Markdown and converted to EPUB

## Output Files

The script generates the following files in the output directory:
- `<video_id>.mp3` - The downloaded audio (if no subtitles were available)
- `<video_id>.raw.txt` - The raw transcript (if transcription was needed)
- `<video_id>.subtitles.txt` - The extracted subtitles (if available)
- `<video_id>.md` - The improved transcript in Markdown format
- `<video_id>.epub` - The improved transcript in EPUB format
