import streamlit as st
import os
from director import generate_scene_director, create_multi_character_dialogue

st.set_page_config(page_title="AI Video Studio", page_icon="🎬")

st.title("🎬 AI Video Studio (Multi-Character Dialogue)")
st.write("Generate custom voice-matched character dialogues directly from your phone!")

# Multi-character image uploads
st.subheader("1. Upload Character Portrets")
col1, col2 = st.columns(2)
with col1:
    char1_img = st.file_uploader("Upload Character 1 (e.g., Host)", type=["jpg", "png", "jpeg"], key="c1")
with col2:
    char2_img = st.file_uploader("Upload Character 2 (e.g., Guest)", type=["jpg", "png", "jpeg"], key="c2")

# Script / Dialogue Input
st.subheader("2. Define Dialogue Script")
dialogue_prompt = st.text_area(
    "Enter dialogue details or conversation topic:",
    "Host: Welcome to the show! Guest: Thanks for having me, let's talk about AI."
)

if st.button("🚀 Generate Dialogue Package"):
    if not char1_img or not char2_img:
        st.error("Please upload both character images to proceed with the dialogue.")
    else:
        with st.spinner("Gemini is structuring the dialogue and synthesizing voices..."):
            # Save uploaded images temporarily
            c1_path = "char1_temp.jpg"
            c2_path = "char2_temp.jpg"
            with open(c1_path, "wb") as f:
                f.write(char1_img.getbuffer())
            with open(c2_path, "wb") as f:
                f.write(char2_img.getbuffer())

            # Generate script and audio tracks via director module
            script_result, audio_files = create_multi_character_dialogue(dialogue_prompt)
            
            st.success("Dialogue script and custom voice tracks created successfully!")
            st.write(script_result)
            
            # Play generated audio tracks
            for idx, audio in enumerate(audio_files):
                st.audio(audio, format="audio/mp3")
                
