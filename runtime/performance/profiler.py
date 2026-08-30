"""
Profiler utilities for Ω-ABSOLUTE foundation components.
Provides function-level profiling and analysis.
"""

from __future__ import annotations

import time
import functools
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
from .performance_monitor import PerformanceMonitor, PerformanceMetric, MetricType


@dataclass
class ProfilingResult:
    """Result of profiling a function or operation"""
    function_name: str
    call_count: int
    total_time: float
    average_time: float
    min_time: float
    max_time: float
    memory_usage_mb: float
    custom_metrics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "function_name": self.function_name,
            "call_count": self.call_count,
            "total_time": self.total_time,
            "average_time": self.average_time,
            "min_time": self.min_time,
            "max_time": self.max_time,
            "memory_usage_mb": self.memory_usage_mb,
            "custom_metrics": self.custom_metrics
        }


class Profiler:
    """
    Function profiler for Ω-ABSOLUTE components.
    Provides timing and memory profiling for functions.
    """
    
    def __init__(self, component_name: str):
        """
        Initialize profiler.
        
        Args:
            component_name: Name of the component being profiled
        """
        self.component_name = component_name
        self.monitor = PerformanceMonitor(component_name)
        self._function_stats: Dict[str, List[float]] = {}
        self._function_memory: Dict[str, List[float]] = {}
    
    def profile_function(self, func: Callable) -> Callable:
        """
        Decorator to profile a function.
        
        Args:
            func: Function to profile
            
        Returns:
            Wrapped function that collects profiling data
            
        Example:
            @profiler.profile_function
            def my_function():
                # code
                pass
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            
            # Profile timing
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            # Store timing stats
            if func_name not in self._function_stats:
                self._function_stats[func_name] = []
            self._function_stats[func_name].append(duration)
            
            # Record with monitor
            self.monitor.record_timing(
                f"function_{func_name}",
                duration,
                {"args": str(args)[:100], "kwargs": str(kwargs)[:100]}
            )
            
            return result
        
        return wrapper
    
    def profile_function_with_memory(self, func: Callable) -> Callable:
        """
        Decorator to profile a function with memory tracking.
        
        Args:
            func: Function to profile
            
        Returns:
            Wrapped function that collects timing and memory data
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            
            # Profile with memory context
            with self.monitor.measure_memory(f"function_memory_{func_name}"):
                with self.monitor.measure_time(f"function_time_{func_name}"):
                    result = func(*args, **kwargs)
            
            return result
        
        return wrapper
    
    def get_function_stats(self, function_name: str) -> Optional[ProfilingResult]:
        """
        Get profiling statistics for a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            ProfilingResult or None if function not profiled
        """
        if function_name not in self._function_stats:
            return None
        
        timings = self._function_stats[function_name]
        memory_metrics = self.monitor.get_metrics(
            metric_type=MetricType.MEMORY,
            name=f"function_memory_{function_name}"
        )
        
        memory_usage = sum(m.value for m in memory_metrics) if memory_metrics else 0.0
        
        return ProfilingResult(
            function_name=function_name,
            call_count=len(timings),
            total_time=sum(timings),
            average_time=sum(timings) / len(timings),
            min_time=min(timings),
            max_time=max(timings),
            memory_usage_mb=memory_usage
        )
    
    def get_all_stats(self) -> List[ProfilingResult]:
        """
        Get profiling statistics for all profiled functions.
        
        Returns:
            List of ProfilingResult for all profiled functions
        """
        results = []
        for function_name in self._function_stats:
            result = self.get_function_stats(function_name)
            if result:
                results.append(result)
        return results
    
    def get_slowest_functions(self, limit: int = 10) -> List[ProfilingResult]:
        """
        Get the slowest functions by average execution time.
        
        Args:
            limit: Maximum number of functions to return
            
        Returns:
            List of ProfilingResult sorted by average time
        """
        all_stats = self.get_all_stats()
        return sorted(all_stats, key=lambda x: x.average_time, reverse=True)[:limit]
    
    def get_most_called_functions(self, limit: int = 10) -> List[ProfilingResult]:
        """
        Get the most frequently called functions.
        
        Args:
            limit: Maximum number of functions to return
            
        Returns:
            List of ProfilingResult sorted by call count
        """
        all_stats = self.get_all_stats()
        return sorted(all_stats, key=lambda x: x.call_count, reverse=True)[:limit]
    
    def reset(self) -> None:
        """Reset all profiling data"""
        self._function_stats.clear()
        self._function_memory.clear()
        self.monitor.clear()
    
    def get_monitor(self) -> PerformanceMonitor:
        """Get the underlying performance monitor"""
        return self.monitor