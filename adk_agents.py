"""
APQR ADK Agents - Legacy Compatibility Module

This module is maintained for backward compatibility.
All agent definitions have been moved to the agents/ package.

New structure:
- agents/orchestrator_agent.py: Root orchestrator
- agents/compiler_agent.py: Response compiler
- agents/lims_domain_agent.py: LIMS coordinator
- agents/erp_domain_agent.py: ERP coordinator
- agents/dms_domain_agent.py: DMS coordinator
- agents/lims/: LIMS sub-agents (QC, Validation, R&D)
- agents/erp/: ERP sub-agents (Manufacturing, Engineering, Supply Chain)
- agents/dms/: DMS sub-agents (QA, Regulatory, Management, Training)

For new code, import directly from agentic_apqr.agents:
    from agentic_apqr.agents import orchestrator_agent, compiler_agent
    from agentic_apqr.agents import lims_agent, erp_agent, dms_agent
"""

# Import all agents for backward compatibility
from agentic_apqr.agents import (
    # Root and Compiler
    orchestrator_agent,
    compiler_agent,
    
    # Domain Agents
    lims_agent,
    erp_agent,
    dms_agent,

# LIMS Sub-Agents
    lims_qc_agent,
    lims_validation_agent,
    lims_rnd_agent,

# ERP Sub-Agents
    erp_manufacturing_agent,
    erp_engineering_agent,
    erp_supplychain_agent,

# DMS Sub-Agents
    dms_qa_agent,
    dms_regulatory_agent,
    dms_management_agent,
    dms_training_agent
)

__all__ = [
    'orchestrator_agent',
    'compiler_agent',
    'lims_agent',
    'erp_agent',
    'dms_agent',
    'lims_qc_agent',
    'lims_validation_agent',
    'lims_rnd_agent',
    'erp_manufacturing_agent',
    'erp_engineering_agent',
    'erp_supplychain_agent',
    'dms_qa_agent',
    'dms_regulatory_agent',
    'dms_management_agent',
    'dms_training_agent'
]
