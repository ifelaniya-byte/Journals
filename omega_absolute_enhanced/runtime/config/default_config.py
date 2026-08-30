"""
Default configuration for Ω-ABSOLUTE foundation.
Provides sensible defaults for all configuration parameters.
"""

from .config_manager import OmegaConfig, ResourceConfig, LoggingConfig, TelemetryConfig, GovernanceConfig


def get_default_config() -> OmegaConfig:
    """
    Get default configuration for Ω-ABSOLUTE foundation.
    
    Returns:
        OmegaConfig with default values suitable for development and testing
    """
    return OmegaConfig(
        resources=ResourceConfig(
            max_tokens_per_task=1_000_000,
            max_wall_time_seconds=3600,
            max_tool_calls=500,
            max_memory_mb=8192,
            max_recursive_critique_depth=5
        ),
        logging=LoggingConfig(
            enabled=True,
            min_level="INFO",
            log_dir=None,  # Will use current directory if not specified
            console_output=True,
            file_output=False,
            max_entries=10000
        ),
        telemetry=TelemetryConfig(
            enabled=True,
            event_buffer_size=1000,
            resource_tracking=True,
            performance_tracking=False
        ),
        governance=GovernanceConfig(
            strict_claim_discipline=True,
            audit_log_enabled=True,
            change_control_required=True,
            rollback_retention_days=30
        )
    )


def get_production_config() -> OmegaConfig:
    """
    Get production-oriented configuration.
    
    Returns:
        OmegaConfig with values suitable for production deployment
    """
    return OmegaConfig(
        resources=ResourceConfig(
            max_tokens_per_task=10_000_000,  # Higher limits for production
            max_wall_time_seconds=7200,  # 2 hours
            max_tool_calls=2000,
            max_memory_mb=16384,  # 16GB
            max_recursive_critique_depth=3  # Lower for production safety
        ),
        logging=LoggingConfig(
            enabled=True,
            min_level="WARNING",  # Less verbose in production
            log_dir="/var/log/omega_absolute",
            console_output=False,
            file_output=True,
            max_entries=100000  # Larger buffer for production
        ),
        telemetry=TelemetryConfig(
            enabled=True,
            event_buffer_size=10000,
            resource_tracking=True,
            performance_tracking=True  # Enable performance tracking in production
        ),
        governance=GovernanceConfig(
            strict_claim_discipline=True,
            audit_log_enabled=True,
            change_control_required=True,
            rollback_retention_days=90  # Longer retention in production
        )
    )


def get_testing_config() -> OmegaConfig:
    """
    Get testing-oriented configuration.
    
    Returns:
        OmegaConfig with values suitable for testing environments
    """
    return OmegaConfig(
        resources=ResourceConfig(
            max_tokens_per_task=100_000,  # Lower limits for testing
            max_wall_time_seconds=300,  # 5 minutes
            max_tool_calls=50,
            max_memory_mb=1024,  # 1GB
            max_recursive_critique_depth=10  # Higher for testing edge cases
        ),
        logging=LoggingConfig(
            enabled=True,
            min_level="DEBUG",  # Verbose logging for testing
            log_dir=None,
            console_output=True,
            file_output=False,
            max_entries=1000  # Smaller buffer for testing
        ),
        telemetry=TelemetryConfig(
            enabled=True,
            event_buffer_size=100,
            resource_tracking=True,
            performance_tracking=True
        ),
        governance=GovernanceConfig(
            strict_claim_discipline=True,
            audit_log_enabled=False,  # Disable audit for faster testing
            change_control_required=False,  # Relax for testing
            rollback_retention_days=1
        )
    )