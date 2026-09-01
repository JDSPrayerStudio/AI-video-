import os
import time
import requests
from google import genai

def generate_scene_director(prompt_text):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable is missing."

    client = genai.Client(api_key=api_key)

    director_prompt = f"""
    You are an expert AI Video Director. 
    Based on this input: '{prompt_text}', write a concise visual prompt (under 40 words) describing the scene visuals for an AI video generator. 
    Focus only on lighting, movement, character appearance, and camera angle.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=director_prompt,
    )
    return response.text.strip()

def render_video_from_prompt(visual_prompt):
    # Free Hugging Face Inference API for Zeroscope Text-to-Video
    API_URL = "https://api-inference.huggingface.co/models/cerspense/zeroscope_v2_576w"
    headers = {"Content-Type": "application/json"}
    payload = {"inputs": visual_prompt}

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        return None
        
