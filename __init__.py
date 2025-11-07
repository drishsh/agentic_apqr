"""
APQR Agentic System - Pharmaceutical Quality Review Automation

A multi-agent system for Annual Product Quality Review (APQR) automation
using Google's Agent Development Kit (ADK).

Main Components:
- Orchestrator Agent: Routes user queries to appropriate domain agents
- Domain Agents: LIMS, ERP, DMS - coordinate specialized sub-agents
- Sub-Agents: Execute specific tools and queries (10 total)
- Compiler Agent: Synthesizes final reports
- Tools: Centralized parsing, OCR, and document extraction utilities

Usage:
    from agentic_apqr import root_agent
    response = root_agent.run("Show me batch quality data for ASP-25-001")
"""

from agentic_apqr.agent import root_agent, orchestrator_agent
from agentic_apqr import tools
from agentic_apqr import agents

__version__ = "2.0.0"

__all__ = [
    'root_agent',
    'orchestrator_agent',
    'tools',
    'agents'
]
