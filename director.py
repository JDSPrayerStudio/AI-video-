import os
from google import genai
from gtts import gTTS

def generate_scene_director(prompt_text):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is missing."

    client = genai.Client(api_key=api_key)
    director_prompt = f"""
    You are an expert AI Dialogue Director. 
    Based on this input: '{prompt_text}', rewrite it into a clear two-person alternating script format starting explicitly with 'Speaker 1:' and 'Speaker 2:'. Keep sentences punchy and optimized for short-form video.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=director_prompt,
    )
    return response.text.strip()

def create_multi_character_dialogue(prompt_text):
    # Step 1: Get structured script from Gemini
    script_text = generate_scene_director(prompt_text)
    
    # Step 2: Split script lines and generate custom audio clips via gTTS
    lines = script_text.split('\n')
    audio_files = []
    
    for i, line in enumerate(lines):
        if line.strip():
            # Generate speech audio matching the exact script line text
            tts = gTTS(text=line, lang='en', slow=False)
            audio_path = f"line_{i}.mp3"
            tts.save(audio_path)
            audio_files.append(audio_path)
            
    return script_text, audio_files
    
