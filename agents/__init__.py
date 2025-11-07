"""
APQR Agents Package
Contains all domain agents, sub-agents, orchestrator, and compiler.

Architecture:
- Orchestrator Agent (TIER 0): Main entry point, routes to domain agents
- Domain Agents (TIER 1): LIMS, ERP, DMS - coordinate their respective sub-agents
- Sub-Agents (TIER 2): Specialized agents with tools for specific tasks
- Compiler Agent (TIER 1): Synthesizes responses and cross-verifies data

Only the Orchestrator and Compiler interact with end users.
All other agents communicate only with their parent agents.
"""

# Import sub-agents
from .lims import lims_qc_agent, lims_validation_agent, lims_rnd_agent
from .erp import erp_manufacturing_agent, erp_engineering_agent, erp_supplychain_agent
from .dms import dms_qa_agent, dms_regulatory_agent, dms_management_agent, dms_training_agent

# Import domain agents
from .lims_domain_agent import lims_agent
from .erp_domain_agent import erp_agent
from .dms_domain_agent import dms_agent

# Import compiler and orchestrator
from .compiler_agent import compiler_agent
from .orchestrator_agent import orchestrator_agent

__all__ = [
    # Root Agent
    'orchestrator_agent',
    
    # Compiler
    'compiler_agent',
    
    # Domain Agents
    'lims_agent',
    'erp_agent',
    'dms_agent',
    
    # LIMS Sub-Agents
    'lims_qc_agent',
    'lims_validation_agent',
    'lims_rnd_agent',
    
    # ERP Sub-Agents
    'erp_manufacturing_agent',
    'erp_engineering_agent',
    'erp_supplychain_agent',
    
    # DMS Sub-Agents
    'dms_qa_agent',
    'dms_regulatory_agent',
    'dms_management_agent',
    'dms_training_agent'
]
