"""
Configuration manager for Ω-ABSOLUTE foundation.
Supports YAML and JSON configuration files with validation.
"""

from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field


class ConfigLoadError(Exception):
    """Raised when configuration file cannot be loaded or is invalid"""
    
    def __init__(self, message: str, file_path: Optional[Path] = None, details: Optional[Dict] = None):
        super().__init__(message)
        self.file_path = file_path
        self.details = details or {}


@dataclass
class ResourceConfig:
    """Configuration for resource ceilings"""
    max_tokens_per_task: int = 1_000_000
    max_wall_time_seconds: int = 3600
    max_tool_calls: int = 500
    max_memory_mb: int = 8192
    max_recursive_critique_depth: int = 5


@dataclass
class LoggingConfig:
    """Configuration for logging system"""
    enabled: bool = True
    min_level: str = "INFO"
    log_dir: Optional[str] = None
    console_output: bool = True
    file_output: bool = False
    max_entries: int = 10000


@dataclass
class TelemetryConfig:
    """Configuration for telemetry system"""
    enabled: bool = True
    event_buffer_size: int = 1000
    resource_tracking: bool = True
    performance_tracking: bool = False


@dataclass
class GovernanceConfig:
    """Configuration for governance system"""
    strict_claim_discipline: bool = True
    audit_log_enabled: bool = True
    change_control_required: bool = True
    rollback_retention_days: int = 30


@dataclass
class OmegaConfig:
    """Main configuration class for Ω-ABSOLUTE"""
    resources: ResourceConfig = field(default_factory=ResourceConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    telemetry: TelemetryConfig = field(default_factory=TelemetryConfig)
    governance: GovernanceConfig = field(default_factory=GovernanceConfig)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "resources": {
                "max_tokens_per_task": self.resources.max_tokens_per_task,
                "max_wall_time_seconds": self.resources.max_wall_time_seconds,
                "max_tool_calls": self.resources.max_tool_calls,
                "max_memory_mb": self.resources.max_memory_mb,
                "max_recursive_critique_depth": self.resources.max_recursive_critique_depth,
            },
            "logging": {
                "enabled": self.logging.enabled,
                "min_level": self.logging.min_level,
                "log_dir": self.logging.log_dir,
                "console_output": self.logging.console_output,
                "file_output": self.logging.file_output,
                "max_entries": self.logging.max_entries,
            },
            "telemetry": {
                "enabled": self.telemetry.enabled,
                "event_buffer_size": self.telemetry.event_buffer_size,
                "resource_tracking": self.telemetry.resource_tracking,
                "performance_tracking": self.telemetry.performance_tracking,
            },
            "governance": {
                "strict_claim_discipline": self.governance.strict_claim_discipline,
                "audit_log_enabled": self.governance.audit_log_enabled,
                "change_control_required": self.governance.change_control_required,
                "rollback_retention_days": self.governance.rollback_retention_days,
            }
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'OmegaConfig':
        """Create configuration from dictionary"""
        resources_data = config_dict.get("resources", {})
        logging_data = config_dict.get("logging", {})
        telemetry_data = config_dict.get("telemetry", {})
        governance_data = config_dict.get("governance", {})
        
        return cls(
            resources=ResourceConfig(**resources_data),
            logging=LoggingConfig(**logging_data),
            telemetry=TelemetryConfig(**telemetry_data),
            governance=GovernanceConfig(**governance_data)
        )


class ConfigManager:
    """Manages loading, validation, and access to configuration"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Optional path to configuration file (YAML or JSON)
        """
        self.config_path = config_path
        self._config: Optional[OmegaConfig] = None
    
    def load(self) -> OmegaConfig:
        """
        Load configuration from file or use defaults.
        
        Returns:
            Loaded OmegaConfig instance
            
        Raises:
            ConfigLoadError: If configuration file cannot be loaded or is invalid
        """
        if self.config_path is None or not self.config_path.exists():
            # Use default configuration
            from .default_config import get_default_config
            self._config = get_default_config()
            return self._config
        
        try:
            config_dict = self._load_file(self.config_path)
            self._config = OmegaConfig.from_dict(config_dict)
            self._validate_config(self._config)
            return self._config
        except Exception as e:
            raise ConfigLoadError(
                f"Failed to load configuration from {self.config_path}: {str(e)}",
                file_path=self.config_path,
                details={"error_type": type(e).__name__}
            )
    
    def _load_file(self, file_path: Path) -> Dict[str, Any]:
        """Load configuration file based on extension"""
        suffix = file_path.suffix.lower()
        
        if suffix == '.json':
            with open(file_path, 'r') as f:
                return json.load(f)
        elif suffix in ['.yaml', '.yml']:
            if not YAML_AVAILABLE:
                raise ConfigLoadError(
                    f"YAML support not available. Install PyYAML or use JSON format.",
                    file_path=file_path,
                    details={"install_hint": "pip install pyyaml"}
                )
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            raise ConfigLoadError(
                f"Unsupported configuration file format: {suffix}",
                file_path=file_path,
                details={"supported_formats": [".json", ".yaml", ".yml"]}
            )
    
    def _validate_config(self, config: OmegaConfig) -> None:
        """Validate configuration values"""
        # Validate resource ceilings
        if config.resources.max_tokens_per_task <= 0:
            raise ConfigLoadError("max_tokens_per_task must be positive")
        if config.resources.max_wall_time_seconds <= 0:
            raise ConfigLoadError("max_wall_time_seconds must be positive")
        if config.resources.max_tool_calls < 0:
            raise ConfigLoadError("max_tool_calls must be non-negative")
        if config.resources.max_memory_mb <= 0:
            raise ConfigLoadError("max_memory_mb must be positive")
        if config.resources.max_recursive_critique_depth < 0:
            raise ConfigLoadError("max_recursive_critique_depth must be non-negative")
        
        # Validate logging configuration
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if config.logging.min_level not in valid_log_levels:
            raise ConfigLoadError(
                f"min_level must be one of {valid_log_levels}",
                details={"provided_level": config.logging.min_level}
            )
        
        if config.logging.max_entries <= 0:
            raise ConfigLoadError("max_entries must be positive")
        
        # Validate telemetry configuration
        if config.telemetry.event_buffer_size <= 0:
            raise ConfigLoadError("event_buffer_size must be positive")
        
        # Validate governance configuration
        if config.governance.rollback_retention_days < 0:
            raise ConfigLoadError("rollback_retention_days must be non-negative")
    
    def get_config(self) -> OmegaConfig:
        """
        Get current configuration.
        
        Returns:
            Current OmegaConfig instance
            
        Raises:
            ConfigLoadError: If configuration has not been loaded
        """
        if self._config is None:
            raise ConfigLoadError("Configuration has not been loaded. Call load() first.")
        return self._config
    
    def save(self, file_path: Path, format: str = "yaml") -> None:
        """
        Save current configuration to file.
        
        Args:
            file_path: Path to save configuration
            format: Format to save ("yaml" or "json")
            
        Raises:
            ConfigLoadError: If configuration has not been loaded or format is invalid
        """
        if self._config is None:
            raise ConfigLoadError("Configuration has not been loaded. Call load() first.")
        
        config_dict = self._config.to_dict()
        
        try:
            if format.lower() == "json":
                with open(file_path, 'w') as f:
                    json.dump(config_dict, f, indent=2)
            elif format.lower() == "yaml":
                if not YAML_AVAILABLE:
                    raise ConfigLoadError(
                        f"YAML support not available. Install PyYAML or use JSON format.",
                        details={"install_hint": "pip install pyyaml"}
                    )
                with open(file_path, 'w') as f:
                    yaml.dump(config_dict, f, default_flow_style=False)
            else:
                raise ConfigLoadError(
                    f"Unsupported save format: {format}",
                    details={"supported_formats": ["json", "yaml"]}
                )
        except Exception as e:
            raise ConfigLoadError(
                f"Failed to save configuration to {file_path}: {str(e)}",
                file_path=file_path,
                details={"error_type": type(e).__name__}
            )
    
    def reload(self) -> OmegaConfig:
        """
        Reload configuration from file.
        
        Returns:
            Reloaded OmegaConfig instance
        """
        self._config = None
        return self.load()