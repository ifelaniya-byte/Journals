"""
Structured logger for Ω-ABSOLUTE foundation components.
Provides consistent, structured logging with context awareness.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional
from pathlib import Path


class LogLevel(Enum):
    """Canonical log levels for Ω-ABSOLUTE"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogContext:
    """Structured context for log entries"""
    component: str
    subsystem: Optional[str] = None
    task_id: Optional[str] = None
    correlation_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: float
    level: LogLevel
    message: str
    context: LogContext
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "level": self.level.value,
            "message": self.message,
            "context": self.context.to_dict(),
            "extra": self.extra
        }


class StructuredLogger:
    """
    Structured logger that integrates with Ω-ABSOLUTE telemetry system.
    Provides consistent logging format across all foundation components.
    """
    
    def __init__(self, 
                 component_name: str,
                 log_file: Optional[Path] = None,
                 console_output: bool = True,
                 min_level: LogLevel = LogLevel.INFO):
        """
        Initialize structured logger.
        
        Args:
            component_name: Name of the component using this logger
            log_file: Optional path to log file
            console_output: Whether to output to console
            min_level: Minimum log level to record
        """
        self.component_name = component_name
        self.min_level = min_level
        self.console_output = console_output
        self.log_file = log_file
        
        # In-memory log storage
        self._entries: List[LogEntry] = []
        
        # Standard Python logger for file/console output
        self._python_logger = logging.getLogger(f"omega.{component_name}")
        self._python_logger.setLevel(min_level.value)
        
        # Remove existing handlers
        self._python_logger.handlers.clear()
        
        # Setup handlers
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(min_level.value)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            self._python_logger.addHandler(console_handler)
        
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(min_level.value)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            self._python_logger.addHandler(file_handler)
    
    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged based on level"""
        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3,
            LogLevel.CRITICAL: 4
        }
        return level_order[level] >= level_order[self.min_level]
    
    def _log(self, 
             level: LogLevel, 
             message: str, 
             context: Optional[LogContext] = None,
             **extra) -> None:
        """
        Internal logging method.
        
        Args:
            level: Log level
            message: Log message
            context: Optional log context
            **extra: Additional structured data
        """
        if not self._should_log(level):
            return
        
        # Create context if not provided
        if context is None:
            context = LogContext(component=self.component_name)
        else:
            # Ensure component is set
            if context.component != self.component_name:
                context = LogContext(
                    component=self.component_name,
                    subsystem=context.subsystem,
                    task_id=context.task_id,
                    correlation_id=context.correlation_id,
                    user_id=context.user_id,
                    session_id=context.session_id,
                    metadata=context.metadata
                )
        
        # Create log entry
        entry = LogEntry(
            timestamp=time.time(),
            level=level,
            message=message,
            context=context,
            extra=extra
        )
        
        # Store in memory
        self._entries.append(entry)
        
        # Output to Python logger
        log_method = getattr(self._python_logger, level.value.lower())
        extra_str = f" | Extra: {json.dumps(extra)}" if extra else ""
        log_method(f"{message}{extra_str}")
    
    def debug(self, message: str, context: Optional[LogContext] = None, **extra) -> None:
        """Log debug message"""
        self._log(LogLevel.DEBUG, message, context, **extra)
    
    def info(self, message: str, context: Optional[LogContext] = None, **extra) -> None:
        """Log info message"""
        self._log(LogLevel.INFO, message, context, **extra)
    
    def warning(self, message: str, context: Optional[LogContext] = None, **extra) -> None:
        """Log warning message"""
        self._log(LogLevel.WARNING, message, context, **extra)
    
    def error(self, message: str, context: Optional[LogContext] = None, **extra) -> None:
        """Log error message"""
        self._log(LogLevel.ERROR, message, context, **extra)
    
    def critical(self, message: str, context: Optional[LogContext] = None, **extra) -> None:
        """Log critical message"""
        self._log(LogLevel.CRITICAL, message, context, **extra)
    
    def get_entries(self, 
                    level: Optional[LogLevel] = None,
                    component: Optional[str] = None,
                    limit: Optional[int] = None) -> List[LogEntry]:
        """
        Retrieve log entries with optional filtering.
        
        Args:
            level: Filter by log level
            component: Filter by component name
            limit: Maximum number of entries to return
            
        Returns:
            List of matching log entries
        """
        entries = self._entries
        
        if level is not None:
            entries = [e for e in entries if e.level == level]
        
        if component is not None:
            entries = [e for e in entries if e.context.component == component]
        
        if limit is not None:
            entries = entries[-limit:]
        
        return entries
    
    def clear(self) -> None:
        """Clear all log entries from memory"""
        self._entries.clear()
    
    def export_json(self, filepath: Path) -> None:
        """
        Export all log entries to JSON file.
        
        Args:
            filepath: Path to output JSON file
        """
        entries_data = [entry.to_dict() for entry in self._entries]
        with open(filepath, 'w') as f:
            json.dump(entries_data, f, indent=2)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get logging statistics.
        
        Returns:
            Dictionary with logging statistics
        """
        level_counts = {}
        for entry in self._entries:
            level = entry.level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            "total_entries": len(self._entries),
            "level_counts": level_counts,
            "component": self.component_name,
            "min_level": self.min_level.value
        }