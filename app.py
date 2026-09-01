import streamlit as st
import os
from director import create_multi_character_dialogue, animate_talking_head

st.set_page_config(page_title="AI Video Studio", page_icon="🎬")

st.title("🎬 AI Video Studio (Multi-Character Dialogue)")
st.write("Generate custom voice-matched character dialogues directly from your phone!")

# Initialize session state so data doesn't wipe on refresh
if "script_result" not in st.session_state:
    st.session_state.script_result = None
if "audio_files" not in st.session_state:
    st.session_state.audio_files = []
if "c1_path" not in st.session_state:
    st.session_state.c1_path = None
if "c2_path" not in st.session_state:
    st.session_state.c2_path = None

# Multi-character image uploads
st.subheader("1. Upload Character Portraits")
col1, col2 = st.columns(2)
with col1:
    char1_img = st.file_uploader("Upload Character 1 (Host)", type=["jpg", "png", "jpeg"], key="c1")
with col2:
    char2_img = st.file_uploader("Upload Character 2 (Guest)", type=["jpg", "png", "jpeg"], key="c2")

# Save images to session state immediately when uploaded
if char1_img:
    st.session_state.c1_path = "char1_temp.jpg"
    with open(st.session_state.c1_path, "wb") as f:
        f.write(char1_img.getbuffer())

if char2_img:
    st.session_state.c2_path = "char2_temp.jpg"
    with open(st.session_state.c2_path, "wb") as f:
        f.write(char2_img.getbuffer())

# Script / Dialogue Input
st.subheader("2. Define Dialogue Script")
dialogue_prompt = st.text_area(
    "Enter dialogue details or conversation topic:",
    "Host: Welcome to the show! Guest: Thanks for having me, let's talk about AI."
)

if st.button("🚀 Generate Dialogue Package"):
    if not st.session_state.c1_path or not st.session_state.c2_path:
        st.error("Please upload both character images to proceed with the dialogue.")
    else:
        with st.spinner("Step 1/2: Gemini is scripting and synthesizing voices..."):
            script_result, audio_files = create_multi_character_dialogue(dialogue_prompt)
            st.session_state.script_result = script_result
            st.session_state.audio_files = audio_files
            st.success("Dialogue script and custom voice tracks created!")

# Display results if they exist in session state
if st.session_state.script_result:
    st.subheader("3. Character Voice & Animation Preview")
    st.write(st.session_state.script_result)
    
    for idx, audio_path in enumerate(st.session_state.audio_files):
        if os.path.exists(audio_path):
            st.write(f"Line {idx + 1} Audio Track:")
            st.audio(audio_path, format="audio/mp3")

            active_image = st.session_state.c1_path if idx % 2 == 0 else st.session_state.c2_path
            char_name = "Character 1 (Host)" if idx % 2 == 0 else "Character 2 (Guest)"

            if st.button(f"Animate Line {idx + 1} for {char_name}", key=f"anim_{idx}"):
                with st.spinner(f"Connecting to Remote GPU Bridge to animate {char_name}..."):
                    video_result = animate_talking_head(active_image, audio_path)
                    if video_result:
                        st.success(f"Animation complete for Line {idx + 1}!")
                        st.video(video_result)
                    else:
                        st.error("Remote GPU bridge timed out or busy. Please try again.")
                        
