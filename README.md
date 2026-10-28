<div align="center">

# 🤖 ALLBEN-AUTONOMOUS-MULTI-AGENT-SOAR-SYSTEM

### *Agentic AI for Enterprise Security Operations*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-FF6B35?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

**A next-generation Security Orchestration, Automation, and Response (SOAR) platform built by [Allben Rakgoale](https://github.com/allben09). Instead of just detecting threats, this system uses a collaborative team of AI Agents to triage, enrich, and respond to SIEM alerts — exactly like a Tier-1 SOC Analyst.**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [The SOC Analyst Problem](#-the-soc-analyst-problem)
- [The 4-Agent Architecture](#-the-4-agent-architecture)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Quick Start](#-quick-start)
- [Security Considerations](#-security-considerations)
- [Roadmap](#-roadmap)
- [Author](#-author)

---

## 🔍 Overview

**ALLBEN-AUTONOMOUS-MULTI-AGENT-SOAR-SYSTEM** is an Agentic AI workflow designed to automate the most repetitive parts of a Security Operations Center (SOC). 

Traditional SOAR platforms rely on rigid "If-This-Then-That" playbooks. This system uses **Large Language Models (LLMs)** to reason through ambiguous alerts, allowing it to adapt to novel threats in real-time. 

Built with **LangGraph**, the system manages a stateful, cyclic workflow where four specialized AI agents collaborate to resolve an incident.

---

## 🎯 The SOC Analyst Problem

> *"SOC Analysts suffer from extreme alert fatigue. 50% of alerts are false positives, and it takes an average of 45 minutes to triage a single alert manually."*

| Challenge | How This System Solves It |
| :--- | :--- |
| **Alert Fatigue** | The Triage Agent instantly filters out low-severity noise. |
| **Context Switching** | The Enrichment Agent automatically queries VirusTotal/AbuseIPDB. |
| **Slow Response** | The Response Agent executes firewall blocks in milliseconds via API. |
| **Weak Defenses** | The **Red Team Agent** evaluates the response and forces an escalation if the defense was insufficient. |

---

## 🏗️ The 4-Agent Architecture

This system uses a custom LangGraph state machine. It does not just run linearly; it **loops** if the defense needs to be escalated.

```text
                    [ SIEM Alert Ingested ]
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ 1. Triage Agent         │
                 │ - Extracts IP & Severity│
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ 2. Enrichment Agent     │
                 │ - Queries Threat Intel  │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ 3. Response Agent       │
                 │ - Blocks IP via API     │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ 4. Red Team Agent       │
                 │ - Evaluates Defense     │
                 └────────────┬────────────┘
                              │
           ┌──────────────────┴──────────────────┐
           │ [Defense Weak?]                     │ [Defense Strong?]
           ▼                                     ▼
  [ Loop back to Agent 3 ]                   [ Incident Closed ]
  (Escalate: Isolate Host)
