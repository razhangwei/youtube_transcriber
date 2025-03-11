import google.generativeai as genai
import os

def improve_transcript(transcript):
    """Improve transcript readability using Gemini"""
    # Get API key from environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # System prompt for improving readability
    system_prompt = """
    You are a transcript editor. Please improve the following YouTube transcript by:
    
    - Improving Paragraphing: Break down long paragraphs into shorter, more digestible paragraphs to enhance visual readability.
    - Using Lists for Key Points: Format lists of items, steps, or key takeaways using bullet points or numbered lists.
    - Removing Filler Words: Eliminate unnecessary filler words and phrases like "you know," "like," "um," "sort of," "basically," "kind of," etc., to create a cleaner and more professional tone.
    - Enhancing Sentence Structure: Improve sentence structure for clarity and conciseness. Correct run-on sentences and awkward phrasing.
    - Emphasizing Key Information: Use bold text or other formatting (if applicable in your context) to highlight headings, subheadings, key terms, or important points for emphasis and scannability.
    - Annotating Non-Verbal Cues (Optional): If there are descriptions of actions, gestures, or non-verbal cues (like laughter, pauses, object usage for illustration), consider adding brief annotations in parentheses or brackets to capture these elements if they are important to the transcript's context.
    
    Format your response in Markdown.
    """
    
    # Create the model with settings matching your preferences
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-thinking-exp-01-21",
        generation_config={
            "temperature": 0.7,    # Adjusted to match your settings
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 65536,  # Increased to match your settings
        },
    )
    
    # Create a chat session with the system prompt
    chat = model.start_chat(history=[
        {
            "role": "user",
            "parts": [system_prompt]
        },
        {
            "role": "model",
            "parts": ["I'll follow these guidelines to improve the transcript's readability."]
        },
    ])
    
    # Send the transcript for improvement
    print(f"Transcript length: {len(transcript)} characters")
    response = chat.send_message(
        f"Here's the transcript to improve:\n\n{transcript}"
    )
    
    return response.text
