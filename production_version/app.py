"""
Streamlit UI — Agentic PPT Builder
------------------------------------
Web interface for the multi-agent PowerPoint presentation generator.
Provides a form-based UI for topic input, configuration, and presentation download.

Usage:
    streamlit run app.py
"""

import streamlit as st
import os
import sys

# Add the current directory to sys.path to resolve local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.orchestrator import run_pipeline
from config.settings import Config
from utils.logger import get_logger
from utils.validators import ValidationError

logger = get_logger(__name__)

st.set_page_config(page_title="Agentic PPT Builder", layout="wide")

st.title("🤖 Agentic AI PowerPoint Builder")
st.markdown("Generate professional presentations using a team of AI agents.")

# ── Sidebar — Configuration Status ──────────────────────────────────
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

    st.divider()
    st.caption(f"v{Config.APP_VERSION}")

# ── Main Form ────────────────────────────────────────────────────────
with st.form("ppt_form"):
    topic = st.text_input(
        "Presentation Topic",
        "Agentic AI in Healthcare",
        max_chars=Config.MAX_TOPIC_LENGTH,
    )
    col1, col2 = st.columns(2)
    with col1:
        num_slides = st.number_input(
            "Number of Slides",
            min_value=Config.MIN_SLIDE_COUNT,
            max_value=Config.MAX_SLIDE_COUNT,
            value=Config.DEFAULT_SLIDE_COUNT,
        )
        font = st.selectbox("Font Style", Config.ALLOWED_FONTS)
    with col2:
        depth = st.selectbox("Content Depth", Config.ALLOWED_DEPTHS, index=1)
        st.markdown("")  # Spacer

    submitted = st.form_submit_button("🚀 Generate Presentation")

if submitted:
    # 1. Configuration Validation
    try:
        Config.validate_keys()
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.stop()

    # 2. Input Validation (handled inside orchestrator, but double-check here)
    if not topic or len(topic.strip()) < Config.MIN_TOPIC_LENGTH:
        st.error(f"Please provide a valid topic (at least {Config.MIN_TOPIC_LENGTH} characters).")
        st.stop()

    with st.status("🚀 Multi-agent pipeline is running...", expanded=True) as status:
        st.write("✅ Initializing agents...")

        try:
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
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    )
            else:
                st.error("Presentation generation returned empty result. Check logs.")
                status.update(label="❌ Generation Failed", state="error")

        except ValidationError as ve:
            st.error(f"Input Error: {str(ve)}")
            status.update(label="❌ Validation Failed", state="error")

        except Exception as e:
            logger.error(f"Critical Application Error: {e}", exc_info=True)
            st.error(f"An unexpected error occurred: {e}")
            status.update(label="❌ System Error", state="error")
