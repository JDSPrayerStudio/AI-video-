import os
import google.generativeai as genai

# Configure Gemini API using environment secret
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def direct_scene(prompt, character_name, age_tone, costume):
    model = genai.GenerativeModel('gemini-1.5-flash')
    full_prompt = (
        f"You are an AI video studio director. "
        f"Character Name: {character_name}, Voice/Age Tone: {age_tone}, Costume: {costume}. "
        f"Based on this script concept: '{prompt}', break it down into precise spoken lines "
        f"and visual directions formatted for video generation."
    )
    
    response = model.generate_content(full_prompt)
    return response.text

if __name__ == "__main__":
    # Test script execution
    print("AI Studio Director Initialized Successfully.")
  
