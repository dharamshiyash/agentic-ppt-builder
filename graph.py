from langgraph.graph import StateGraph, END
from state import AgentState
from agents.planner.agent import planner_agent
from agents.writer.agent import writer_agent
from agents.image.agent import image_agent
from agents.builder.agent import builder_agent 

def build_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("planner", planner_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("image_agent", image_agent)
    workflow.add_node("ppt_builder", builder_agent) # Note: Node name matched to app.py expectation

    # Add Edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "writer")
    workflow.add_edge("writer", "image_agent")
    workflow.add_edge("image_agent", "ppt_builder")
    workflow.add_edge("ppt_builder", END)

    return workflow.compile()
