import streamlit as st
import os
from director import create_multi_character_dialogue

st.set_page_config(page_title="AI Video Studio", page_icon="🎬")

st.title("🎬 AI Video Studio (Mobile Optimized)")
st.write("No more crashes. Manage your AI character scripts and custom voice tracks smoothly.")

# Session state persistence
if "script_result" not in st.session_state:
    st.session_state.script_result = None
if "audio_files" not in st.session_state:
    st.session_state.audio_files = []

# Character Portrait URL Inputs (Crash-proof on mobile)
st.subheader("1. Character Image Links")
st.write("Paste direct image URLs (e.g., from Pinterest, Imgur, or a public link) for your characters:")
col1, col2 = st.columns(2)
with col1:
    char1_img = st.text_input("Character 1 Image URL", "https://images.unsplash.com/photo-1534528741775-53994a69daeb")
with col2:
    char2_img = st.text_input("Character 2 Image URL", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d")

# Script / Dialogue Input
st.subheader("2. Dialogue Script Generator")
dialogue_prompt = st.text_area(
    "Enter your conversation topic or script idea:",
    "Host: Welcome to the show! Guest: Thanks for having me, let's talk about AI tech."
)

if st.button("🚀 Generate Dialogue & Voice Tracks"):
    if not char1_img or not char2_img:
        st.error("Please provide both character image URLs.")
    else:
        with st.spinner("Gemini is building your script and generating voices..."):
            script_result, audio_files = create_multi_character_dialogue(dialogue_prompt)
            st.session_state.script_result = script_result
            st.session_state.audio_files = audio_files
            st.success("Dialogue package created successfully!")

# Display generated workspace
if st.session_state.script_result:
    st.subheader("3. Production Script & Audio Assets")
    st.text_area("Final Script Output:", st.session_state.script_result, height=150)
    
    st.write("### Voice-Over Previews")
    for idx, audio_path in enumerate(st.session_state.audio_files):
        if os.path.exists(audio_path):
            speaker_label = "Character 1 (Host)" if idx % 2 == 0 else "Character 2 (Guest)"
            st.write(f"Audio Track {idx + 1} — {speaker_label}")
            st.audio(audio_path, format="audio/mp3")
            
