# YouTube Subtitle Extractor

A tool to extract and enhance existing YouTube subtitles for better readability.

## Features

- Extract existing English subtitles from YouTube videos
- Post-process subtitles with Gemini AI to improve readability
- Output both Markdown and EPUB formats

## Requirements

- Python 3.7+
- API keys:
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

3. Set up API keys by creating a `.env` file:
```
cp .env.example .env
```
Then edit the `.env` file to add your API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
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

### Gemini Model Configuration

You can customize the Gemini model's behavior with these options:

```
--model MODEL_NAME        # Default: gemini-2.5-flash-preview-05-20
--temperature TEMP        # Controls randomness (0.0 to 1.0), default: 0.2
--top-p TOP_P             # Nucleus sampling, default: 0.95
--top-k TOP_K             # Top-k sampling, default: 0
--max-tokens TOKENS       # Max tokens in response, default: 65536
```

Example with custom model settings:
```
python main.py https://www.youtube.com/watch?v=XXXXXXXXXXX \
  --gemini-model gemini-1.5-pro \
  --gemini-temperature 0.7 \
  --gemini-max-tokens 8192
```

### API Key Configuration

1. Using command line arguments (overrides .env):
```
python main.py https://www.youtube.com/watch?v=XXXXXXXXXXX --gemini-api-key YOUR_KEY
```

2. Using a custom .env file:
```
python main.py https://www.youtube.com/watch?v=XXXXXXXXXXX --env-file /path/to/custom/.env
```

## How It Works

1. The script checks if the YouTube video has existing English subtitles
2. If subtitles exist, they are extracted and post-processed with Gemini AI to:
   - Improve paragraphing
   - Format lists properly
   - Remove filler words
   - Enhance sentence structure
   - Emphasize key information
   - Add annotations for non-verbal cues
4. The improved transcript is saved as Markdown and converted to EPUB

## Output Files

The script generates the following files in the output directory:
- `<video_id>.subtitles.txt` - The extracted subtitles
- `<video_id>.md` - The improved transcript in Markdown format
- `<video_id>.epub` - The improved transcript in EPUB format
