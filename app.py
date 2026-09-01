import streamlit as st
import os
from director import create_multi_character_dialogue, animate_talking_head

st.set_page_config(page_title="AI Video Studio", page_icon="🎬")

st.title("🎬 AI Video Studio (Mobile Form Mode)")
st.write("Select both character photos and type your script inside the form without mid-selection refreshes.")

# Initialize session state
if "script_result" not in st.session_state:
    st.session_state.script_result = None
if "audio_files" not in st.session_state:
    st.session_state.audio_files = []
if "c1_path" not in st.session_state:
    st.session_state.c1_path = None
if "c2_path" not in st.session_state:
    st.session_state.c2_path = None

# Wrap inputs in a form to prevent mobile resets between file selections
with st.form("studio_form"):
    st.subheader("1. Character Photos & Script")
    col1, col2 = st.columns(2)
    with col1:
        char1_img = st.file_uploader("Character 1 (Host)", type=["jpg", "png", "jpeg"], key="c1_upload")
    with col2:
        char2_img = st.file_uploader("Character 2 (Guest)", type=["jpg", "png", "jpeg"], key="c2_upload")

    dialogue_prompt = st.text_area(
        "Enter your conversation topic or script idea:",
        "Host: Welcome to the show! Guest: Thanks for having me, let's talk about AI tech."
    )
    
    submitted = st.form_submit_button("🚀 Generate Dialogue & Voice Tracks")

# Process form submission
if submitted:
    if not char1_img or not char2_img:
        st.error("Please make sure both character photos are selected inside the form before submitting.")
    else:
        # Save uploaded files safely to session state paths
        st.session_state.c1_path = "char1_temp.jpg"
        with open(st.session_state.c1_path, "wb") as f:
            f.write(char1_img.getbuffer())

        st.session_state.c2_path = "char2_temp.jpg"
        with open(st.session_state.c2_path, "wb") as f:
            f.write(char2_img.getbuffer())

        with st.spinner("Building script and generating custom voice tracks..."):
            script_result, audio_files = create_multi_character_dialogue(dialogue_prompt)
            st.session_state.script_result = script_result
            st.session_state.audio_files = audio_files
            st.success("Dialogue package created successfully!")

# Display generated workspace & video generation buttons outside the form
if st.session_state.script_result:
    st.subheader("3. Production Script, Audio & Video Generation")
    st.text_area("Final Script Output:", st.session_state.script_result, height=150, key="script_output_display")
    
    for idx, audio_path in enumerate(st.session_state.audio_files):
        if os.path.exists(audio_path):
            speaker_label = "Character 1 (Host)" if idx % 2 == 0 else "Character 2 (Guest)"
            active_image = st.session_state.c1_path if idx % 2 == 0 else st.session_state.c2_path
            
            st.write("---")
            st.write(f"**Line {idx + 1} — {speaker_label}**")
            st.audio(audio_path, format="audio/mp3")
            
            if st.button(f"🎬 Generate Talking Video for Line {idx + 1}", key=f"anim_btn_{idx}"):
                with st.spinner(f"Connecting to Remote GPU to animate {speaker_label}..."):
                    video_result = animate_talking_head(active_image, audio_path)
                    if video_result:
                        st.success(f"Video generated successfully for Line {idx + 1}!")
                        st.video(video_result)
                    else:
                        st.error("Remote GPU space is currently busy or timed out. Please tap again.")
                        
