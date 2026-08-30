"""
Log formatter for Ω-ABSOLUTE structured logging.
Provides consistent formatting across different output targets.
"""

from __future__ import annotations

import json
from typing import Dict, Any
from .structured_logger import LogEntry, LogLevel


class LogFormatter:
    """Formatter for structured log entries"""
    
    @staticmethod
    def format_console(entry: LogEntry) -> str:
        """
        Format log entry for console output.
        
        Args:
            entry: Log entry to format
            
        Returns:
            Formatted string for console
        """
        context_str = f"[{entry.context.component}"
        if entry.context.subsystem:
            context_str += f"/{entry.context.subsystem}"
        if entry.context.task_id:
            context_str += f" task:{entry.context.task_id}"
        context_str += "]"
        
        extra_str = ""
        if entry.extra:
            extra_str = f" | {json.dumps(entry.extra)}"
        
        return f"{entry.level.value:8} {context_str} {entry.message}{extra_str}"
    
    @staticmethod
    def format_json(entry: LogEntry) -> str:
        """
        Format log entry as JSON string.
        
        Args:
            entry: Log entry to format
            
        Returns:
            JSON string representation
        """
        return json.dumps(entry.to_dict())
    
    @staticmethod
    def format_structured(entry: LogEntry) -> Dict[str, Any]:
        """
        Format log entry as structured dictionary.
        
        Args:
            entry: Log entry to format
            
        Returns:
            Structured dictionary representation
        """
        return entry.to_dict()
    
    @staticmethod
    def format_summary(entries: list) -> str:
        """
        Format a summary of multiple log entries.
        
        Args:
            entries: List of log entries
            
        Returns:
            Summary string
        """
        if not entries:
            return "No log entries"
        
        level_counts = {}
        for entry in entries:
            level = entry.level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        summary_lines = [
            f"Total entries: {len(entries)}",
            "Level breakdown:"
        ]
        for level, count in sorted(level_counts.items()):
            summary_lines.append(f"  {level}: {count}")
        
        return "\n".join(summary_lines)