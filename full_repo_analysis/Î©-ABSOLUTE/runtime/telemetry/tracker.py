"""
Resource Tracker and Telemetry Bus – §56, §57.
Every major subsystem SHOULD expose resource telemetry.
Core enforces resource ceilings via OmegaCore.check_resource.
"""

from __future__ import annotations

from typing import Callable, List, Optional

from .events import TelemetryEvent, ResourceUsage
from runtime.core.omega_core import OmegaCore, CoreViolationError


class TelemetryBus:
    """Simple in-memory bus. Production systems may replace with structured logging."""

    def __init__(self) -> None:
        self._events: List[TelemetryEvent] = []
        self._subscribers: List[Callable[[TelemetryEvent], None]] = []

    def publish(self, event: TelemetryEvent) -> None:
        self._events.append(event)
        for sub in self._subscribers:
            try:
                sub(event)
            except Exception:
                # Telemetry failures must not crash the main loop
                pass

    def subscribe(self, callback: Callable[[TelemetryEvent], None]) -> None:
        self._subscribers.append(callback)

    def get_events(self, subsystem: Optional[str] = None) -> List[TelemetryEvent]:
        if subsystem is None:
            return list(self._events)
        return [e for e in self._events if e.subsystem == subsystem]

    def clear(self) -> None:
        self._events.clear()


class ResourceTracker:
    """
    Tracks cumulative resource usage for a task or subsystem
    and enforces Core ceilings.
    """

    def __init__(self, core: OmegaCore, bus: Optional[TelemetryBus] = None) -> None:
        self._core = core
        self._bus = bus or TelemetryBus()
        self._current = ResourceUsage()

    @property
    def current(self) -> ResourceUsage:
        return self._current

    def record(self, usage: ResourceUsage, subsystem: str, action: str) -> None:
        """Merge usage and enforce ceilings. Raises CoreViolationError on breach."""
        # Check individual ceilings before merging
        if usage.tokens:
            self._core.check_resource("max_tokens_per_task", self._current.tokens + usage.tokens)
        if usage.wall_time_seconds:
            self._core.check_resource("max_wall_time_seconds", self._current.wall_time_seconds + usage.wall_time_seconds)
        if usage.tool_calls:
            self._core.check_resource("max_tool_calls", self._current.tool_calls + usage.tool_calls)
        if usage.memory_mb:
            self._core.check_resource("max_memory_mb", max(self._current.memory_mb, usage.memory_mb))

        self._current = self._current.merge(usage)

        event = TelemetryEvent(
            subsystem=subsystem,
            action=action,
            resource_usage=usage,
        )
        self._bus.publish(event)

    def snapshot(self) -> ResourceUsage:
        return ResourceUsage(**self._current.to_dict())
