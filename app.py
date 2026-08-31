import streamlit as st
import os
from director import direct_scene

st.set_page_config(page_title="AI Video Studio", page_icon="🎬")

st.title("🎬 AI Video Studio (Forever Free)")
st.markdown("Build and direct your videos for Facebook monetization straight from your phone.")

# Sidebar / Input Configuration for Characters
st.sidebar.header("👤 Character Settings")
character_name = st.sidebar.text_input("Character Name", value="Arthur")
age_tone = st.sidebar.selectbox("Voice Tone / Age", ["Old Man", "Young Child", "Adult Male", "Adult Female"])
costume = st.sidebar.text_input("Costume Description", value="Red jacket and blue jeans")

# Main Script Prompt Section
st.header("📝 Scene Director Script")
prompt = st.text_area("Describe what the character should say or do in this scene:", value="Welcome back to my channel, today we are talking about motivation and success.")

if st.button("🚀 Direct Scene with Gemini"):
    if not os.environ.get("GEMINI_API_KEY") and "GEMINI_API_KEY" not in st.secrets:
        # Allow inputting API key dynamically if not set as environment variable
        api_key_input = st.text_input("Enter your Gemini API Key:", type="password")
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input
    
    try:
        with st.spinner("Director Gemini is crafting your scene..."):
            result = direct_scene(prompt, character_name, age_tone, costume)
            st.success("Scene Script Generated Successfully!")
            st.write(result)
    except Exception as e:
        st.error(f"Error: {e}. Please ensure your Gemini API key is configured.")
      
