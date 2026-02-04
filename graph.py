from langgraph.graph import StateGraph, END
from agentic_ppt_builder.state import AgentState
from agentic_ppt_builder.agents.planner_agent import planner_agent
from agentic_ppt_builder.agents.writer_agent import writer_agent
from agentic_ppt_builder.agents.image_agent import image_agent
from agentic_ppt_builder.agents.ppt_builder_agent import ppt_builder_agent

def build_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("planner", planner_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("image_agent", image_agent)
    workflow.add_node("ppt_builder", ppt_builder_agent)

    # Add Edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "writer")
    workflow.add_edge("writer", "image_agent")
    workflow.add_edge("image_agent", "ppt_builder")
    workflow.add_edge("ppt_builder", END)

    return workflow.compile()
