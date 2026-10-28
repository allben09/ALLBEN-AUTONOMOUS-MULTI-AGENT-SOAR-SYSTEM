"""
src/agents.py
The individual AI agents (Triage, Enrichment, Response, Red Team).
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .state import SOCState

# Initialize the LLM (You can swap this for ChatGroq if you have a Groq API key)
# It requires OPENAI_API_KEY in your environment variables
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

def triage_agent(state: SOCState):
    """Agent 1: Analyzes the raw alert and assigns severity."""
    alert = state["alert"]
    
    prompt = f"""
    You are a Tier-1 SOC Analyst. Analyze this raw SIEM alert:
    {alert}
    
    Extract the source IP and summarize the threat in one sentence.
    Assign a severity level (LOW, MEDIUM, HIGH, CRITICAL).
    Format output strictly as: [SEVERITY] - [IP] - [Summary]
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    content = response.content
    
    # Simple parsing (in a real app, use Pydantic structured output)
    parts = content.split(" - ")
    severity = parts[0].strip("[] ")
    target_ip = parts[1].strip()
    summary = parts[2]
    
    return {
        "severity": severity,
        "target_ip": target_ip,
        "triage_summary": summary,
        "logs": [f"🔍 Triage Agent: Detected {severity} threat from {target_ip}."]
    }

def enrichment_agent(state: SOCState):
    """Agent 2: Enriches the alert with Threat Intel."""
    ip = state["target_ip"]
    
    # MOCK API CALL (In production, call VirusTotal or AbuseIPDB here)
    # We simulate that IPs starting with "185." are malicious
    is_malicious = ip.startswith("185.220") or ip.startswith("45.142")
    
    threat_intel = {
        "ip": ip,
        "is_malicious": is_malicious,
        "reports": 42 if is_malicious else 0,
        "source": "AbuseIPDB (Mock)"
    }
    
    feedback = f"🌐 Enrichment Agent: {ip} has {threat_intel['reports']} abuse reports. Malicious: {is_malicious}"
    return {
        "threat_intel": threat_intel,
        "logs": [feedback]
    }

def response_agent(state: SOCState):
    """Agent 3: Decides and executes a response playbook."""
    intel = state["threat_intel"]
    red_team_feedback = state.get("red_team_feedback", "")
    
    # If the Red Team said the action was bad, escalate the action
    if red_team_feedback:
        action = "BLOCK_IP_AND_ISOLATE_HOST"
        action_desc = "Escalated: Blocked IP and isolated the local host."
    elif intel["is_malicious"]:
        action = "BLOCK_IP"
        action_desc = "Blocked the malicious IP at the firewall."
    else:
        action = "MONITOR"
        action_desc = "IP not malicious. Increased monitoring."
        
    return {
        "proposed_action": action,
        "action_taken": action_desc,
        "logs": [f"🛡️ Response Agent: {action_desc}"]
    }

def red_team_agent(state: SOCState):
    """Agent 4: Evaluates if the response was sufficient. Can trigger a loop."""
    action = state["proposed_action"]
    severity = state["severity"]
    
    # Logic: If severity is HIGH but we only blocked the IP, the Red Team complains.
    if severity in ["HIGH", "CRITICAL"] and action == "BLOCK_IP":
        feedback = "Blocking the IP is insufficient for a CRITICAL alert. Attacker may pivot. Need to isolate host."
        return {
            "red_team_feedback": feedback,
            "logs": [f"🔴 Red Team: {feedback}"]
        }
    
    # Action was good
    return {
        "red_team_feedback": "",
        "logs": ["✅ Red Team: Response acceptable. Closing incident."]
    }
