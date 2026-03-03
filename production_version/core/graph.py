"""
LangGraph Pipeline Definition
------------------------------
Builds the multi-agent workflow as a directed acyclic graph (DAG).
The pipeline executes agents in a strict linear order:

    PlannerAgent → ResearchAgent → WriterAgent → ImageAgent → BuilderAgent

Each node receives the shared AgentState and returns partial updates
that are merged back into the state before the next node runs.

Usage:
    from core.graph import build_graph
    app = build_graph()
    result = app.invoke(initial_state)
"""

from langgraph.graph import StateGraph, END
from core.state import AgentState
from agents.planner.agent import planner_agent
from agents.research.agent import research_agent
from agents.writer.agent import writer_agent
from agents.image.agent import image_agent
from agents.builder.agent import builder_agent
from utils.logger import get_logger

logger = get_logger(__name__)


def build_graph():
    """
    Construct and compile the LangGraph multi-agent pipeline.

    Returns:
        CompiledGraph: A compiled LangGraph application ready to invoke.

    Pipeline Nodes:
        - planner: Generates slide outline from topic
        - research: Gathers web facts for each slide
        - writer: Writes detailed slide content
        - image_agent: Sources images for each slide
        - ppt_builder: Assembles the final .pptx file
    """
    logger.info("Building multi-agent pipeline graph...")

    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("planner", planner_agent)
    workflow.add_node("research", research_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("image_agent", image_agent)
    workflow.add_node("ppt_builder", builder_agent)

    # Add Edges — 5-agent linear pipeline
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "research")
    workflow.add_edge("research", "writer")
    workflow.add_edge("writer", "image_agent")
    workflow.add_edge("image_agent", "ppt_builder")
    workflow.add_edge("ppt_builder", END)

    logger.info("Pipeline graph compiled successfully.")
    return workflow.compile()
