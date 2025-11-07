"""
Configuration package for APQR system.
Handles loading and management of system configuration.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config file. If None, uses default agents_config.yaml
        
    Returns:
        Dictionary containing configuration
    """
    if config_path is None:
        config_path = Path(__file__).parent / "agents_config.yaml"
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def get_agent_config(agent_name: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Get configuration for a specific agent.
    
    Args:
        agent_name: Name of the agent (lims, erp, dms)
        config: Optional config dictionary. If None, loads from default file
        
    Returns:
        Dictionary containing agent-specific configuration
    """
    if config is None:
        config = load_config()
    
    agents_config = config.get("agents", {})
    return agents_config.get(agent_name.lower(), {})


__all__ = ["load_config", "get_agent_config"]

