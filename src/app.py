"""
src/app.py
Streamlit UI for the Autonomous SOAR System.
"""
import streamlit as st
import os
from dotenv import load_dotenv

from siem_mock import generate_mock_alert
from graph import build_soc_graph

# Load API keys
load_dotenv()

st.set_page_config(page_title="Autonomous SOAR", page_icon="🤖", layout="wide")

st.title("🤖 Allben Autonomous SOAR")
st.caption("Multi-Agent Security Orchestration, Automation & Response | Built by Allben Rakgoale")

if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ Please set your OPENAI_API_KEY in a `.env` file to run the LLM agents.")
    st.stop()

# Sidebar
st.sidebar.header("⚙️ SIEM Control")
if st.sidebar.button("🚨 Simulate New SIEM Alert"):
    st.session_state.alert = generate_mock_alert()
    st.session_state.logs = []
    st.session_state.finished = False

if "alert" not in st.session_state:
    st.session_state.alert = None

# Main Interface
if st.session_state.alert:
    st.info(f"📥 **Raw Alert from SIEM:** {st.session_state.alert}")
    
    if st.button("▶️ Run SOAR Playbook"):
        graph = build_soc_graph()
        
        # Initial state
        initial_state = {
            "alert": st.session_state.alert,
            "logs": []
        }
        
        with st.spinner("Agents are collaborating..."):
            # Run the graph
            final_state = graph.invoke(initial_state)
            
        st.success("✅ Incident Resolved!")
        
        # Display Logs
        st.subheader("🧠 Agent Thought Process")
        for log in final_state["logs"]:
            if "Triage" in log: st.write(f"🟦 {log}")
            elif "Enrichment" in log: st.write(f"🟨 {log}")
            elif "Response" in log: st.write(f"🟩 {log}")
            elif "Red Team" in log: st.write(f"🟥 {log}")
            
        # Final Summary
        st.subheader("📊 Final Incident Report")
        col1, col2, col3 = st.columns(3)
        col1.metric("Severity", final_state.get("severity", "N/A"))
        col1.metric("Target IP", final_state.get("target_ip", "N/A"))
        col3.metric("Action Taken", final_state.get("action_taken", "N/A"))

else:
    st.info("Click 'Simulate New SIEM Alert' on the left to start.")
