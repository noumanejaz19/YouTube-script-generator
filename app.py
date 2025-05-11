"""
YouTube Script Generator - Streamlit Application
"""

import streamlit as st
import os
from utils.script_generator import ScriptGenerator
from utils.text_processor import split_into_segments, count_words, insert_ctas
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state
if 'script' not in st.session_state:
    st.session_state.script = None
if 'segments' not in st.session_state:
    st.session_state.segments = []
if 'title' not in st.session_state:
    st.session_state.title = ""
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""

# Set page config
st.set_page_config(
    page_title="YouTube Script Generator",
    page_icon="��",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🎥 YouTube Script Generator")
    st.markdown("""
    Generate engaging YouTube scripts with AI. Just provide a title and transcript, 
    and let our AI create a professional script for your video.
    """)

    # Initialize script generator
    try:
        script_generator = ScriptGenerator()
    except ValueError as e:
        st.error(f"Error initializing script generator: {str(e)}")
        st.info("Please make sure your OpenAI API key is properly configured in the environment variables.")
        return

    # Input fields
    with st.form("script_form"):
        title = st.text_input("Video Title", placeholder="Enter your video title")
        transcript = st.text_area("Inspirational Video Transcript", 
                                placeholder="Paste the transcript of the video that inspired you",
                                height=200)
        word_count = st.slider("Desired Word Count", 
                             min_value=1000, 
                             max_value=10000, 
                             value=5000, 
                             step=500)
        
        submitted = st.form_submit_button("Generate Script")

    if submitted:
        if not title or not transcript:
            st.warning("Please fill in all fields")
            return

        with st.spinner("Generating your script..."):
            try:
                script = script_generator.generate_script(title, transcript, word_count)
                if script:
                    st.success("Script generated successfully!")
                    st.markdown("### Generated Script")
                    st.markdown(script)
                    
                    # Add download button
                    st.download_button(
                        label="Download Script",
                        data=script,
                        file_name=f"{title.lower().replace(' ', '_')}_script.md",
                        mime="text/markdown"
                    )
                else:
                    st.error("Failed to generate script. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

# Display generated script
if st.session_state.script:
    st.subheader("Generated Script")
    
    # Display word count
    total_words = count_words(st.session_state.script)
    st.info(f"Total word count: {total_words}")
    
    # Display segments
    for i, segment in enumerate(st.session_state.segments):
        st.markdown(f"### Segment {i + 1}")
        st.text_area(
            f"Segment {i + 1}",
            value=segment,
            height=200,
            key=f"segment_{i}"
        )
        
        # Regenerate button for each segment
        if st.button(f"Regenerate Segment {i + 1}", key=f"regenerate_{i}"):
            with st.spinner(f"Regenerating segment {i + 1}..."):
                new_segment = script_generator.regenerate_segment(
                    st.session_state.title,
                    st.session_state.transcript,
                    i,
                    st.session_state.segments
                )
                
                if new_segment:
                    st.session_state.segments[i] = new_segment
                    st.experimental_rerun()
                else:
                    st.error(f"Failed to regenerate segment {i + 1}. Please try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>YouTube Script Generator | Powered by Claude AI</p>
</div>
""", unsafe_allow_html=True) 