import streamlit as st
import os
from director import create_multi_character_dialogue, animate_talking_head

st.set_page_config(page_title="AI Video Studio", page_icon="🎬")

st.title("🎬 AI Video Studio (Mobile Gallery Mode)")
st.write("Upload character photos, build dialogue, and animate your talking heads.")

# Initialize session state
if "script_result" not in st.session_state:
    st.session_state.script_result = None
if "audio_files" not in st.session_state:
    st.session_state.audio_files = []
if "c1_path" not in st.session_state:
    st.session_state.c1_path = None
if "c2_path" not in st.session_state:
    st.session_state.c2_path = None

# Character Portrait File Uploads
st.subheader("1. Upload Character Photos")
col1, col2 = st.columns(2)
with col1:
    char1_img = st.file_uploader("Character 1 (Host)", type=["jpg", "png", "jpeg"], key="c1_upload")
with col2:
    char2_img = st.file_uploader("Character 2 (Guest)", type=["jpg", "png", "jpeg"], key="c2_upload")

if char1_img is not None:
    st.session_state.c1_path = "char1_temp.jpg"
    with open(st.session_state.c1_path, "wb") as f:
        f.write(char1_img.getbuffer())

if char2_img is not None:
    st.session_state.c2_path = "char2_temp.jpg"
    with open(st.session_state.c2_path, "wb") as f:
        f.write(char2_img.getbuffer())

if st.session_state.c1_path and st.session_state.c2_path:
    st.success("✅ Both character photos loaded into your studio memory!")

# Script / Dialogue Input
st.subheader("2. Define Dialogue Script")
dialogue_prompt = st.text_area(
    "Enter your conversation topic or script idea:",
    "Host: Welcome to the show! Guest: Thanks for having me, let's talk about AI tech."
)

if st.button("🚀 Generate Dialogue & Voice Tracks"):
    if not st.session_state.c1_path or not st.session_state.c2_path:
        st.error("Please upload both character photos first before generating.")
    else:
        with st.spinner("Building script and generating custom voice tracks..."):
            script_result, audio_files = create_multi_character_dialogue(dialogue_prompt)
            st.session_state.script_result = script_result
            st.session_state.audio_files = audio_files
            st.success("Dialogue package created successfully!")

# Display generated workspace & video generation buttons
if st.session_state.script_result:
    st.subheader("3. Production Script, Audio & Video Generation")
    st.text_area("Final Script Output:", st.session_state.script_result, height=150)
    
    for idx, audio_path in enumerate(st.session_state.audio_files):
        if os.path.exists(audio_path):
            speaker_label = "Character 1 (Host)" if idx % 2 == 0 else "Character 2 (Guest)"
            active_image = st.session_state.c1_path if idx % 2 == 0 else st.session_state.c2_path
            
            st.write(f"---")
            st.write(f"**Line {idx + 1} — {speaker_label}**")
            st.audio(audio_path, format="audio/mp3")
            
            # The restored video generation button
            if st.button(f"🎬 Generate Talking Video for Line {idx + 1}", key=f"anim_btn_{idx}"):
                with st.spinner(f"Connecting to Remote GPU to animate {speaker_label}..."):
                    video_result = animate_talking_head(active_image, audio_path)
                    if video_result:
                        st.success(f"Video generated successfully for Line {idx + 1}!")
                        st.video(video_result)
                    else:
                        st.error("Remote GPU space is currently busy or timed out. Please tap again.")
                    
