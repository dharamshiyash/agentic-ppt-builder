import streamlit as st
import os
import shutil
import sys
# Add the current directory to sys.path to resolve local imports correctly on Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph import build_graph
from utils.config import Config
from utils.logger import get_logger

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
    try:
        Config.validate_keys()
    except ValueError as e:
        st.error(str(e))
        st.stop()
    else:
        status_container = st.container()
        
        with st.status("🚀 Agents are working...", expanded=True) as status:
            st.write("Initializing agents...")
            
            # Initialize Graph
            app = build_graph()
            
            initial_state = {
                "topic": topic,
                "slide_count": num_slides,
                "font": font,
                "depth": depth,
                "presentation_outline": [],
                "slide_content": [],
                "final_ppt_path": ""
            }
            
            st.write("📝 **Planner Agent** is structuring the presentation...")
            # We can stream output or just run invoke
            # For better UX, let's invoke and assume progress based on steps implies simple wait
            # If we want granular updates, we could stream events.
            
            try:
                # Running the graph
                # Using invoke for simplicity, as stream might be overkill for this initial version
                # But to update UI we can try to inspect output at each step if we iterate manually? 
                # LangGraph `stream` method is best.
                
                final_state = None
                for output in app.stream(initial_state):
                    for key, value in output.items():
                        if key == "planner":
                            st.write("✅ **Planner Agent**: Outline created.")
                            with st.expander("See Outline"):
                                st.json(value.get("presentation_outline"))
                        elif key == "writer":
                            st.write("✅ **Writer Agent**: Content written.")
                        elif key == "image_agent":
                            st.write("✅ **Image Agent**: Images selected.")
                        elif key == "ppt_builder":
                            st.write("✅ **PPT Builder**: File generated.")
                            final_state = value
                
                if final_state and "final_ppt_path" in final_state:
                    ppt_path = final_state["final_ppt_path"]
                    status.update(label="🎉 Presentation Ready!", state="complete", expanded=False)
                    
                    st.success(f"Presentation generated successfully: {topic}")
                    
                    with open(ppt_path, "rb") as file:
                        btn = st.download_button(
                            label="📥 Download .pptx",
                            data=file,
                            file_name=os.path.basename(ppt_path),
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        )
                        
            except Exception as e:
                st.error(f"An error occurred: {e}")
                status.update(label="❌ Generation Failed", state="error")
