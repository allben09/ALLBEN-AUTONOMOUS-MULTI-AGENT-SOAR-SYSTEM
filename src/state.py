"""
src/state.py
Defines the shared state for the multi-agent SOAR system.
"""
from typing import TypedDict, List, Dict, Annotated
import operator

class SOCState(TypedDict):
    """The shared state passed between agents in the graph."""
    # The raw alert data from the SIEM
    alert: Dict
    
    # Triage output
    triage_summary: str
    severity: str
    target_ip: str
    
    # Enrichment output (Threat Intel)
    threat_intel: Dict
    
    # Response output
    proposed_action: str
    action_taken: str
    
    # Red Team feedback (if the action was insufficient)
    red_team_feedback: str
    
    # Track the conversation/thought process for the UI
    logs: Annotated[List[str], operator.add]
