"""
APQR Root Agent (Orchestrator) - Main Entry Point
This module provides the main entry point for the APQR Agentic System.

The orchestrator agent routes user queries to appropriate domain agents
(LIMS, ERP, DMS) and coordinates response compilation.

Architecture:
- orchestrator_agent: Main entry point (interacts with users)
- Domain agents (LIMS, ERP, DMS): Coordinate specialized sub-agents
- Sub-agents: Execute specific tools and return structured data
- compiler_agent: Synthesizes final user-friendly report (interacts with users)

User Interaction Flow:
User -> Orchestrator -> Domain Agents -> Sub-Agents -> Compiler -> User

CRITICAL: Only Orchestrator and Compiler interact with users.
All other agents communicate only with their parent agents.
"""

from agentic_apqr.agents import orchestrator_agent

# Export the root agent
root_agent = orchestrator_agent

__all__ = ['root_agent', 'orchestrator_agent']
