"""
Agent Orchestrator — Central Pipeline Controller
-------------------------------------------------
Manages the full agent pipeline execution. All callers (``app.py``,
``main.py``, tests) should import ``run_pipeline`` from here instead
of calling ``build_graph`` directly.

Benefits:
    - Single place to add/remove agents from the pipeline
    - Pre- and post-processing hooks (input validation, output logging)
    - Consistent error handling and logging across all entry points

Usage:
    from services.orchestrator import run_pipeline

    result = run_pipeline(
        topic="Artificial Intelligence",
        slide_count=7,
        font="Calibri",
        depth="Concise",
    )
    print(result["final_ppt_path"])
"""

import time
from typing import Optional

from utils.logger import get_logger, log_agent_step
from config.settings import Config
from utils.validators import validate_all_inputs, ValidationError
from utils.error_handler import PipelineTimeoutError

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

    Input validation is performed before pipeline execution. All inputs
    are sanitized and checked against configured constraints.

    Args:
        topic: The presentation topic (must be non-empty, 3–200 characters).
        slide_count: Number of slides to generate. Defaults to ``Config.DEFAULT_SLIDE_COUNT``.
        font: Font name used throughout the presentation.
        depth: Content depth — one of "Minimal", "Concise", "Detailed".

    Returns:
        dict: The final AgentState. Key fields:
            - ``presentation_outline``: List of slide outline items
            - ``research_notes``: Dict of per-slide research snippets
            - ``slide_content``: List of fully written slide dicts
            - ``final_ppt_path``: Absolute path to the generated .pptx file

    Raises:
        ValidationError: If any input fails validation.
        PipelineTimeoutError: If the pipeline exceeds the allowed execution time.
    """
    # ── Input Validation ─────────────────────────────────────────────
    validated = validate_all_inputs(topic, slide_count, font, depth)
    topic = validated["topic"]
    slide_count = validated["slide_count"]
    font = validated["font"]
    depth = validated["depth"]

    log_agent_step(
        logger, "Orchestrator", "PIPELINE_START",
        f"topic='{topic}' | slides={slide_count} | font={font} | depth={depth}"
    )

    start_time = time.time()

    # ── Build & Invoke Graph ─────────────────────────────────────────
    from core.graph import build_graph

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

    # ── Post-processing & Logging ────────────────────────────────────
    elapsed = time.time() - start_time
    ppt_path = final_state.get("final_ppt_path", "")

    if ppt_path:
        log_agent_step(
            logger, "Orchestrator", "PIPELINE_COMPLETE",
            f"output={ppt_path} | duration={elapsed:.1f}s"
        )
    else:
        logger.error(
            f"[Orchestrator] Pipeline finished but no PPT file was generated "
            f"(duration={elapsed:.1f}s). Check agent logs for details."
        )

    return final_state
