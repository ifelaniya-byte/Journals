"""
Integration utilities for connecting structured logging with existing Ω-ABSOLUTE components.
"""

from __future__ import annotations

from typing import Optional
from pathlib import Path

from .structured_logger import StructuredLogger, LogLevel, LogContext
from runtime.telemetry.tracker import TelemetryBus


class LoggingIntegration:
    """Integration utilities for logging system"""
    
    @staticmethod
    def create_component_logger(component_name: str,
                                log_dir: Optional[Path] = None,
                                enable_console: bool = True) -> StructuredLogger:
        """
        Create a logger for a foundation component.
        
        Args:
            component_name: Name of the component
            log_dir: Optional directory for log files
            enable_console: Whether to enable console output
            
        Returns:
            Configured StructuredLogger instance
        """
        log_file = None
        if log_dir:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"{component_name}.log"
        
        return StructuredLogger(
            component_name=component_name,
            log_file=log_file,
            console_output=enable_console,
            min_level=LogLevel.INFO
        )
    
    @staticmethod
    def integrate_with_telemetry(logger: StructuredLogger, 
                                  telemetry_bus: TelemetryBus) -> None:
        """
        Integrate logger with telemetry bus for unified observability.
        
        Args:
            logger: StructuredLogger instance
            telemetry_bus: TelemetryBus instance
        """
        def log_telemetry_event(event):
            """Callback to log telemetry events"""
            logger.info(
                f"Telemetry event: {event.action}",
                subsystem=event.subsystem,
                event_id=str(event.event_id),
                resource_usage=event.resource_usage.to_dict() if event.resource_usage else {}
            )
        
        telemetry_bus.subscribe(log_telemetry_event)
    
    @staticmethod
    def create_core_logger(log_dir: Optional[Path] = None) -> StructuredLogger:
        """Create logger specifically for Core component"""
        return LoggingIntegration.create_component_logger(
            "omega_core",
            log_dir,
            enable_console=True
        )
    
    @staticmethod
    def create_governance_logger(log_dir: Optional[Path] = None) -> StructuredLogger:
        """Create logger specifically for Governance components"""
        return LoggingIntegration.create_component_logger(
            "omega_governance",
            log_dir,
            enable_console=True
        )
    
    @staticmethod
    def create_telemetry_logger(log_dir: Optional[Path] = None) -> StructuredLogger:
        """Create logger specifically for Telemetry components"""
        return LoggingIntegration.create_component_logger(
            "omega_telemetry",
            log_dir,
            enable_console=True
        )