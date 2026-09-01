import streamlit as st
from director import generate_scene_director, render_video_from_prompt

st.set_page_config(page_title="AI Video Studio", page_icon="🎬")
st.title("🎬 AI Video Studio (Forever Free)")
st.write("Generate downloadable videos directly from your phone for Facebook!")

user_input = st.text_area(
    "Describe your video scene:", 
    "A confident presenter speaking in a modern cozy studio, high quality, cinematic lighting."
)

if st.button("🚀 Generate & Render Video"):
    with st.spinner("Step 1/2: Generating visual direction with Gemini..."):
        visual_prompt = generate_scene_director(user_input)
        st.info(f"**Visual Prompt:** {visual_prompt}")
    
    with st.spinner("Step 2/2: Rendering MP4 Video (this takes 1-2 mins)..."):
        video_bytes = render_video_from_prompt(visual_prompt)
        if video_bytes:
            st.success("Video Rendered Successfully!")
            st.video(video_bytes)
            st.download_button(
                label="📥 Download Video (MP4)",
                data=video_bytes,
                file_name="facebook_scene.mp4",
                mime="video/mp4"
            )
        else:
            st.error("Video model is currently warming up on Hugging Face. Please tap generate again in 30 seconds!")
            
