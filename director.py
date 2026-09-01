import os
from google import genai
from gtts import gTTS
from gradio_client import Client

def generate_scene_director(prompt_text):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is missing."

    client = genai.Client(api_key=api_key)
    director_prompt = f"""
    You are an expert AI Dialogue Director. 
    Based on this input: '{prompt_text}', rewrite it into a clear short dialogue format with individual spoken lines. Keep sentences punchy.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=director_prompt,
    )
    return response.text.strip()

def create_multi_character_dialogue(prompt_text):
    script_text = generate_scene_director(prompt_text)
    lines = script_text.split('\n')
    audio_files = []
    
    for i, line in enumerate(lines):
        if line.strip():
            tts = gTTS(text=line, lang='en', slow=False)
            audio_path = f"line_{i}.mp3"
            tts.save(audio_path)
            audio_files.append(audio_path)
            
    return script_text, audio_files

def animate_talking_head(image_path, audio_path):
    try:
        # Connects to a free public GPU space for face animation
        client = Client("KlingTeam/LivePortrait")
        result = client.predict(
            source_image=image_path,
            driving_audio=audio_path,
            api_name="/predict"
        )
        return result
    except Exception as e:
        return None
        
    return script_text, audio_files
    
