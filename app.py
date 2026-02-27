import streamlit as st
import os
import sys

# Add the current directory to sys.path to resolve local imports correctly on Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.agent_controller import run_pipeline
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="Agentic PPT Builder", layout="wide")

st.title("🤖 Agentic AI PowerPoint Builder")
st.markdown("Generate professional presentations using a team of AI agents.")

# Sidebar — API Key Status
with st.sidebar:
    st.header("⚙️ Configuration")
    if Config.GROQ_API_KEY:
        st.success("✅ GROQ API Key loaded")
    else:
        st.error("❌ GROQ_API_KEY missing! Check .env")

    if Config.OPENAI_API_KEY:
        st.success("✅ OpenAI API Key loaded (DALL-E enabled)")
    else:
        st.warning("⚠️ OPENAI_API_KEY not set — will use Unsplash/placeholder images")

    if Config.UNSPLASH_ACCESS_KEY:
        st.success("✅ Unsplash API Key loaded")
    else:
        st.warning("⚠️ UNSPLASH_ACCESS_KEY not set — will use placeholder images")

    st.divider()
    st.markdown("**Agent Pipeline:**")
    st.markdown(
        "1. 🧠 **PlannerAgent** — outlines slides\n"
        "2. 🔍 **ResearchAgent** — gathers web facts\n"
        "3. ✍️ **WriterAgent** — writes slide content\n"
        "4. 🖼️ **ImageAgent** — sources images\n"
        "5. 🏗️ **BuilderAgent** — creates .pptx"
    )

# Main form
with st.form("ppt_form"):
    topic = st.text_input("Presentation Topic", "Agentic AI in Healthcare")
    col1, col2 = st.columns(2)
    with col1:
        num_slides = st.number_input("Number of Slides", min_value=1, max_value=20, value=Config.DEFAULT_SLIDE_COUNT)
        font = st.selectbox("Font Style", ["Arial", "Calibri", "Times New Roman", "Consolas"])
    with col2:
        depth = st.selectbox("Content Depth", ["Minimal", "Concise", "Detailed"], index=1)
        st.markdown("")  # Spacer

    submitted = st.form_submit_button("🚀 Generate Presentation")

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

    with st.status("🚀 Multi-agent pipeline is running...", expanded=True) as status:
        st.write("✅ Initializing agents...")

        try:
            # Human-in-the-loop checkpoint: user already confirmed input via form above
            st.write("🧠 [1/5] PlannerAgent — planning slide outline...")
            st.write("🔍 [2/5] ResearchAgent — gathering web research...")
            st.write("✍️ [3/5] WriterAgent — generating slide content...")
            st.write("🖼️ [4/5] ImageAgent — sourcing images...")
            st.write("🏗️ [5/5] BuilderAgent — assembling .pptx file...")

            # Run through central orchestrator
            final_state = run_pipeline(
                topic=topic,
                slide_count=num_slides,
                font=font,
                depth=depth,
            )

            # Result Handling
            if final_state and final_state.get("final_ppt_path"):
                ppt_path = final_state["final_ppt_path"]
                status.update(label="🎉 Presentation Ready!", state="complete", expanded=False)

                st.success(f"✅ Presentation generated: **{topic}**")

                with open(ppt_path, "rb") as file:
                    st.download_button(
                        label="📥 Download .pptx",
                        data=file,
                        file_name=os.path.basename(ppt_path),
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
            else:
                st.error("Presentation generation returned empty result. Check logs.")
                status.update(label="❌ Generation Failed", state="error")

        except Exception as e:
            logger.error(f"Critical Application Error: {e}", exc_info=True)
            st.error(f"An unexpected error occurred: {e}")
            status.update(label="❌ System Error", state="error")
