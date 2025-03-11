import requests
import os
import json
from pathlib import Path

def transcribe_audio(audio_path):
    """Transcribe audio using Wizper API from fal.ai"""
    api_url = "https://api.fal.ai/models/fal-ai/wizper"
    
    # Get API key from environment variable
    api_key = os.environ.get("FAL_AI_API_KEY")
    if not api_key:
        raise ValueError("FAL_AI_API_KEY environment variable not set")
    
    # Prepare the file for upload
    with open(audio_path, "rb") as f:
        files = {"audio_file": (os.path.basename(audio_path), f, "audio/mpeg")}
        headers = {"Authorization": f"Key {api_key}"}
        
        # Make the API request with a timeout
        response = requests.post(
            api_url, 
            files=files, 
            headers=headers,
            timeout=600  # 10 minutes timeout for large files
        )
        
        if response.status_code != 200:
            error_message = f"API call failed with status {response.status_code}"
            try:
                error_message += f": {response.json().get('error', response.text)}"
            except:
                error_message += f": {response.text}"
            raise Exception(error_message)
        
        result = response.json()
        return result.get("transcript", "")
