import google.generativeai as genai
import os

def improve_transcript(transcript, model_name="gemini-2.5-flash-preview-05-20", temperature=0.2, top_p=0.95, top_k=0, max_output_tokens=65536, system_prompt=None):
    """Improve transcript readability using Gemini
    
    Args:
        transcript (str): The transcript text to improve
        model_name (str): Name of the Gemini model to use
        temperature (float): Controls randomness (0.0 to 1.0)
        top_p (float): Nucleus sampling parameter
        top_k (int): Top-k sampling parameter
        max_output_tokens (int): Maximum number of tokens in the response
        system_prompt (str, optional): Custom system prompt. If None, uses default.
    
    Returns:
        str: Improved transcript text
    """
    # Get API key from environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Default system prompt for improving readability
    default_system_prompt = """
    You are a transcript editor. Please improve the following YouTube transcript by:
    
    - Improving Paragraphing: Break down long paragraphs into shorter, more digestible paragraphs to enhance visual readability.
    - Using Lists for Key Points: Format lists of items, steps, or key takeaways using bullet points or numbered lists.
    - Removing Filler Words: Eliminate unnecessary filler words and phrases like "you know," "like," "um," "sort of," "basically," "kind of," etc., to create a cleaner and more professional tone.
    - Enhancing Sentence Structure: Improve sentence structure for clarity and conciseness. Correct run-on sentences and awkward phrasing.
    - Emphasizing Key Information: Use bold text or other formatting (if applicable in your context) to highlight headings, subheadings, key terms, or important points for emphasis and scannability.
    - Annotating Non-Verbal Cues (Optional): If there are descriptions of actions, gestures, or non-verbal cues (like laughter, pauses, object usage for illustration), consider adding brief annotations in parentheses or brackets to capture these elements if they are important to the transcript's context.
    
    Format your response in Markdown. Only include the improved transcript, no additional text.
    """
    
    # Use custom prompt if provided, otherwise use default
    system_prompt = system_prompt or default_system_prompt
    
    # Create the model with provided or default settings
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
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
