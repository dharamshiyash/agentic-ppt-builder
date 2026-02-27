"""
Agent Controller — Central Orchestrator
----------------------------------------
Manages the full agent pipeline execution. All callers (app.py, main.py, tests)
should import `run_pipeline` from here instead of calling `build_graph` directly.

Benefits:
- Single place to add/remove agents from the pipeline
- Pre- and post-processing hooks (input validation, output logging)
- Consistent error handling and logging across all entrypoints
"""
import os
from typing import Optional
from utils.logger import get_logger
from utils.config import Config
from utils.error_handler import safe_run

logger = get_logger(__name__)


def run_pipeline(
    topic: str,
    slide_count: int = None,
    font: str = "Calibri",
    depth: str = "Concise",
) -> dict:
    """
    Execute the full multi-agent pipeline and return the final AgentState.

    Pipeline:
        PlannerAgent → ResearchAgent → WriterAgent → ImageAgent → BuilderAgent

    Args:
        topic: The presentation topic (must be non-empty, ≥3 characters).
        slide_count: Number of slides to generate. Defaults to Config.DEFAULT_SLIDE_COUNT.
        font: Font name used throughout the presentation.
        depth: Content depth — one of "Minimal", "Concise", "Detailed".

    Returns:
        The final AgentState dict. Key fields:
          - presentation_outline: List of slide outline items
          - research_notes: Dict of per-slide research snippets
          - slide_content: List of fully written slide dicts
          - final_ppt_path: Absolute path to the generated .pptx file

    Raises:
        ValueError: If topic is empty or too short.
    """
    # --- Input Validation ---
    if not topic or len(topic.strip()) < 3:
        raise ValueError("Topic must be at least 3 characters long.")

    slide_count = slide_count or Config.DEFAULT_SLIDE_COUNT
    topic = topic.strip()

    logger.info(
        f"[Orchestrator] Starting pipeline | topic='{topic}' | slides={slide_count} | "
        f"font={font} | depth={depth}"
    )

    # --- Build & Invoke Graph ---
    from graph import build_graph

    app = build_graph()

    initial_state = {
        "topic": topic,
        "slide_count": slide_count,
        "font": font,
        "depth": depth,
        "presentation_outline": [],
        "research_notes": {},
        "slide_content": [],
        "final_ppt_path": "",
    }

    final_state = app.invoke(initial_state)

    # --- Post-processing Logging ---
    ppt_path = final_state.get("final_ppt_path", "")
    if ppt_path:
        logger.info(f"[Orchestrator] Pipeline complete. Output: {ppt_path}")
    else:
        logger.error("[Orchestrator] Pipeline finished but no PPT file was generated.")

    return final_state
