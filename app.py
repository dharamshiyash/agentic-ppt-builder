import streamlit as st
import os
import shutil
import sys
import time

# Add the current directory to sys.path to resolve local imports correctly on Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph import build_graph
from utils.config import Config
from utils.logger import get_logger
from tools.async_queue import enqueue_job

logger = get_logger(__name__)

st.set_page_config(page_title="Agentic PPT Builder", layout="wide")

st.title("🤖 Agentic AI PowerPoint Builder")
st.markdown("Generate professional presentations using a team of AI agents.")

# Sidebar for basic inputs
with st.sidebar:
    st.header("Configuration")
    if Config.GROQ_API_KEY:
        st.success("API Keys loaded successfully")
    else:
        st.error("API Keys missing! Check .env")

def run_pipeline(topic, slide_count, font, depth):
    """
    Wrapper function to run the graph pipeline.
    This is the function that gets enqueued.
    """
    logger.info(f"Starting pipeline for topic: {topic}")
    app = build_graph()
    
    initial_state = {
        "topic": topic,
        "slide_count": slide_count,
        "font": font,
        "depth": depth,
        "presentation_outline": [],
        "slide_content": [],
        "final_ppt_path": ""
    }
    
    # Run the graph
    final_state = app.invoke(initial_state)
    return final_state

# Main form
with st.form("ppt_form"):
    topic = st.text_input("Presentation Topic", "Agentic AI in Healthcare")
    col1, col2 = st.columns(2)
    with col1:
        num_slides = st.number_input("Number of Slides", min_value=1, max_value=20, value=Config.DEFAULT_SLIDE_COUNT)
        font = st.selectbox("Font Style", ["Arial", "Calibri", "Times New Roman", "Consolas"])
    with col2:
        depth = st.selectbox("Content Depth", ["Minimal", "Concise", "Detailed"], index=1)
        include_images = st.checkbox("Include AI-selected Images", value=True)
    
    submitted = st.form_submit_button("Generate Presentation")

if submitted:
    # 1. Configuration Validation
    try:
        Config.validate_keys()
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.stop()
        
    # 2. Input Validation
    if not topic or len(topic.strip()) < 3:
        st.error("Please provide a valid topic (at least 3 characters).")
        st.stop()

    status_container = st.container()
    
    with st.status("🚀 Agents are working...", expanded=True) as status:
        st.write("Initializing agents...")
        
        # 3. Async Execution Integration
        try:
            # Enqueue job (or run sync fallback)
            job, is_async = enqueue_job(run_pipeline, topic, num_slides, font, depth)
            
            if is_async:
                st.write(f"Job enqueued (ID: {job.id}). Waiting for workers...")
                # Poll for completion
                while not job.is_finished:
                    time.sleep(2)
                    job.refresh()
                    if job.is_failed:
                        st.error("Job failed during execution.")
                        st.stop()
                
                final_state = job.result
            else:
                st.write("Running synchronously (Internal fallback)...")
                final_state = job.result
            
            # 4. Result Handling
            if final_state and "final_ppt_path" in final_state and final_state["final_ppt_path"]:
                ppt_path = final_state["final_ppt_path"]
                status.update(label="🎉 Presentation Ready!", state="complete", expanded=False)
                
                st.success(f"Presentation generated successfully: {topic}")
                
                with open(ppt_path, "rb") as file:
                    st.download_button(
                        label="📥 Download .pptx",
                        data=file,
                        file_name=os.path.basename(ppt_path),
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
            else:
                st.error("Presentation generation returned empty result.")
                status.update(label="❌ Generation Failed", state="error")
                
        except Exception as e:
            logger.error(f"Critical Application Error: {e}", exc_info=True)
            st.error(f"An unexpected error occurred: {e}")
            status.update(label="❌ System Error", state="error")
