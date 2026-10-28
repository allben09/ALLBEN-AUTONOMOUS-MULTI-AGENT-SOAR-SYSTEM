"""
src/graph.py
Builds the LangGraph state machine.
"""
from langgraph.graph import StateGraph, END
from .state import SOCState
from .agents import (
    triage_agent, enrichment_agent, response_agent, red_team_agent
)

def build_soc_graph():
    workflow = StateGraph(SOCState)
    
    # Add the nodes (Agents)
    workflow.add_node("triage", triage_agent)
    workflow.add_node("enrich", enrichment_agent)
    workflow.add_node("respond", response_agent)
    workflow.add_node("red_team", red_team_agent)
    
    # Define the flow
    workflow.set_entry_point("triage")
    workflow.add_edge("triage", "enrich")
    workflow.add_edge("enrich", "respond")
    workflow.add_edge("respond", "red_team")
    
    # Conditional edge: Does the Red Team approve?
    def should_escalate(state: SOCState):
        if state.get("red_team_feedback"):
            return "escalate" # Loop back to response agent
        return "end"
        
    workflow.add_conditional_edges(
        "red_team",
        should_escalate,
        {
            "escalate": "respond", # Loop back to Response Agent
            "end": END
        }
    )
    
    return workflow.compile()
