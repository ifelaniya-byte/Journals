"""
Performance monitor for Ω-ABSOLUTE foundation components.
Provides timing, memory tracking, and performance metrics collection.
"""

from __future__ import annotations

import time
import tracemalloc
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Callable, Any
from contextlib import contextmanager


class MetricType(Enum):
    """Types of performance metrics"""
    TIMING = "timing"
    MEMORY = "memory"
    CUSTOM = "custom"


@dataclass
class PerformanceMetric:
    """Single performance metric"""
    name: str
    metric_type: MetricType
    value: float
    unit: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary"""
        return {
            "name": self.name,
            "type": self.metric_type.value,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }


class PerformanceMonitor:
    """
    Performance monitoring system for foundation components.
    Tracks timing, memory usage, and custom metrics.
    """
    
    def __init__(self, component_name: str):
        """
        Initialize performance monitor.
        
        Args:
            component_name: Name of the component being monitored
        """
        self.component_name = component_name
        self._metrics: List[PerformanceMetric] = []
        self._current_memory_baseline: Optional[int] = None
        self._timing_contexts: Dict[str, float] = {}
    
    def record_timing(self, name: str, duration: float, metadata: Optional[Dict] = None) -> None:
        """
        Record a timing metric.
        
        Args:
            name: Name of the timing metric
            duration: Duration in seconds
            metadata: Optional metadata about the measurement
        """
        metric = PerformanceMetric(
            name=name,
            metric_type=MetricType.TIMING,
            value=duration,
            unit="seconds",
            timestamp=time.time(),
            metadata=metadata or {}
        )
        self._metrics.append(metric)
    
    def record_memory(self, name: str, memory_mb: float, metadata: Optional[Dict] = None) -> None:
        """
        Record a memory metric.
        
        Args:
            name: Name of the memory metric
            memory_mb: Memory usage in megabytes
            metadata: Optional metadata about the measurement
        """
        metric = PerformanceMetric(
            name=name,
            metric_type=MetricType.MEMORY,
            value=memory_mb,
            unit="MB",
            timestamp=time.time(),
            metadata=metadata or {}
        )
        self._metrics.append(metric)
    
    def record_custom(self, name: str, value: float, unit: str, metadata: Optional[Dict] = None) -> None:
        """
        Record a custom metric.
        
        Args:
            name: Name of the custom metric
            value: Metric value
            unit: Unit of measurement
            metadata: Optional metadata about the measurement
        """
        metric = PerformanceMetric(
            name=name,
            metric_type=MetricType.CUSTOM,
            value=value,
            unit=unit,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        self._metrics.append(metric)
    
    @contextmanager
    def measure_time(self, name: str, metadata: Optional[Dict] = None):
        """
        Context manager for measuring execution time.
        
        Args:
            name: Name for the timing metric
            metadata: Optional metadata to include
            
        Yields:
            None
            
        Example:
            with monitor.measure_time("operation_x"):
                # do operation
                pass
        """
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.record_timing(name, duration, metadata)
    
    @contextmanager
    def measure_memory(self, name: str, metadata: Optional[Dict] = None):
        """
        Context manager for measuring memory usage.
        
        Args:
            name: Name for the memory metric
            metadata: Optional metadata to include
            
        Yields:
            None
            
        Example:
            with monitor.measure_memory("operation_x"):
                # do operation
                pass
        """
        tracemalloc.start()
        if self._current_memory_baseline is None:
            self._current_memory_baseline = tracemalloc.get_traced_memory()[0]
        
        try:
            yield
        finally:
            current, peak = tracemalloc.get_traced_memory()
            memory_mb = (current - self._current_memory_baseline) / (1024 * 1024)
            self.record_memory(name, memory_mb, metadata)
            tracemalloc.stop()
            self._current_memory_baseline = None
    
    def start_timing(self, name: str) -> None:
        """
        Start a manual timing measurement.
        
        Args:
            name: Name for the timing metric
        """
        self._timing_contexts[name] = time.time()
    
    def stop_timing(self, name: str, metadata: Optional[Dict] = None) -> float:
        """
        Stop a manual timing measurement and record it.
        
        Args:
            name: Name of the timing metric (must match start_timing call)
            metadata: Optional metadata to include
            
        Returns:
            Duration in seconds
            
        Raises:
            KeyError: If timing context not found
        """
        if name not in self._timing_contexts:
            raise KeyError(f"No timing context found for '{name}'")
        
        start_time = self._timing_contexts.pop(name)
        duration = time.time() - start_time
        self.record_timing(name, duration, metadata)
        return duration
    
    def get_metrics(self, 
                   metric_type: Optional[MetricType] = None,
                   name: Optional[str] = None,
                   limit: Optional[int] = None) -> List[PerformanceMetric]:
        """
        Retrieve metrics with optional filtering.
        
        Args:
            metric_type: Filter by metric type
            name: Filter by metric name
            limit: Maximum number of metrics to return
            
        Returns:
            List of matching performance metrics
        """
        metrics = self._metrics
        
        if metric_type is not None:
            metrics = [m for m in metrics if m.metric_type == metric_type]
        
        if name is not None:
            metrics = [m for m in metrics if m.name == name]
        
        if limit is not None:
            metrics = metrics[-limit:]
        
        return metrics
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get performance statistics.
        
        Returns:
            Dictionary with performance statistics
        """
        if not self._metrics:
            return {
                "component": self.component_name,
                "total_metrics": 0,
                "by_type": {},
                "timing_stats": {},
                "memory_stats": {}
            }
        
        # Count by type
        type_counts = {}
        for metric in self._metrics:
            metric_type = metric.metric_type.value
            type_counts[metric_type] = type_counts.get(metric_type, 0) + 1
        
        # Timing statistics
        timing_metrics = [m for m in self._metrics if m.metric_type == MetricType.TIMING]
        timing_stats = {}
        if timing_metrics:
            values = [m.value for m in timing_metrics]
            timing_stats = {
                "count": len(values),
                "total": sum(values),
                "average": sum(values) / len(values),
                "min": min(values),
                "max": max(values)
            }
        
        # Memory statistics
        memory_metrics = [m for m in self._metrics if m.metric_type == MetricType.MEMORY]
        memory_stats = {}
        if memory_metrics:
            values = [m.value for m in memory_metrics]
            memory_stats = {
                "count": len(values),
                "total": sum(values),
                "average": sum(values) / len(values),
                "min": min(values),
                "max": max(values)
            }
        
        return {
            "component": self.component_name,
            "total_metrics": len(self._metrics),
            "by_type": type_counts,
            "timing_stats": timing_stats,
            "memory_stats": memory_stats
        }
    
    def clear(self) -> None:
        """Clear all recorded metrics"""
        self._metrics.clear()
        self._timing_contexts.clear()
    
    def export_json(self, filepath: str) -> None:
        """
        Export all metrics to JSON file.
        
        Args:
            filepath: Path to output JSON file
        """
        import json
        metrics_data = [metric.to_dict() for metric in self._metrics]
        with open(filepath, 'w') as f:
            json.dump(metrics_data, f, indent=2)
    
    def get_slowest_operations(self, limit: int = 10) -> List[PerformanceMetric]:
        """
        Get the slowest timing operations.
        
        Args:
            limit: Maximum number of operations to return
            
        Returns:
            List of slowest timing metrics sorted by duration
        """
        timing_metrics = [m for m in self._metrics if m.metric_type == MetricType.TIMING]
        return sorted(timing_metrics, key=lambda x: x.value, reverse=True)[:limit]
    
    def get_memory_intensive_operations(self, limit: int = 10) -> List[PerformanceMetric]:
        """
        Get the most memory-intensive operations.
        
        Args:
            limit: Maximum number of operations to return
            
        Returns:
            List of most memory-intensive metrics sorted by memory usage
        """
        memory_metrics = [m for m in self._metrics if m.metric_type == MetricType.MEMORY]
        return sorted(memory_metrics, key=lambda x: x.value, reverse=True)[:limit]