"""
Configuration management system for Ω-ABSOLUTE foundation.
Provides external configuration support for resource ceilings, logging, and other parameters.
"""

from .config_manager import ConfigManager, ConfigLoadError
from .default_config import get_default_config

__all__ = ['ConfigManager', 'ConfigLoadError', 'get_default_config']