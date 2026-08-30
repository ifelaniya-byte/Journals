#!/usr/bin/env python3
"""
API demonstration script showing usage of key Ω-ABSOLUTE foundation APIs.
"""

import sys
from pathlib import Path

# Add runtime to path
sys.path.insert(0, str(Path(__file__).parent))

def demo_core_api():
    """Demonstrate Core API"""
    print("CORE API DEMONSTRATION")
    print("=" * 50)
    
    from runtime.core.omega_core import OmegaCore, CoreViolationError
    
    core = OmegaCore()
    
    print(f"Identity: {core.identity}")
    print(f"Formal Name: {core.formal_name}")
    print(f"Version: {core.core_version}")
    
    # Resource checking
    try:
        core.check_resource("max_tokens_per_task", 100)
        print("✓ Resource check passed (100 tokens)")
    except CoreViolationError as e:
        print(f"✗ Resource violation: {e}")
    
    try:
        core.check_resource("max_tokens_per_task", 2_000_000)
        print("✗ Resource check should have failed")
    except CoreViolationError as e:
        print(f"✓ Resource violation caught: {e.violation_type}")
    
    print()


def demo_governance_api():
    """Demonstrate Governance API"""
    print("GOVERNANCE API DEMONSTRATION")
    print("=" * 50)
    
    from runtime.governance.claim_discipline import ClaimDiscipline, ClaimViolationError
    from runtime.governance.states import DevelopmentState, ClaimLevel
    
    disc = ClaimDiscipline()
    
    # Register component
    disc.register("test.component", DevelopmentState.IMPLEMENTED)
    print(f"✓ Registered test.component at {DevelopmentState.IMPLEMENTED.value}")
    
    # Test claim discipline
    try:
        disc.assert_claim_allowed("test.component", ClaimLevel.VERIFICATION)
        print("✗ Claim check should have failed")
    except ClaimViolationError as e:
        print(f"✓ Claim violation caught: {e.component_id}")
        print(f"  Claimed: {e.claimed_level}, Actual: {e.actual_state}")
    
    # Safe status string
    status = disc.safe_status_string("test.component")
    print(f"✓ Safe status: {status}")
    
    print()


def demo_telemetry_api():
    """Demonstrate Telemetry API"""
    print("TELEMETRY API DEMONSTRATION")
    print("=" * 50)
    
    from runtime import get_core
    from runtime.telemetry.tracker import TelemetryBus, ResourceTracker
    from runtime.telemetry.events import ResourceUsage
    
    core = get_core()
    bus = TelemetryBus()
    tracker = ResourceTracker(core, bus)
    
    # Record resource usage
    tracker.record(ResourceUsage(tokens=100, tool_calls=2), "demo", "operation")
    print(f"✓ Recorded resource usage")
    print(f"  Tokens: {tracker.current.tokens}")
    print(f"  Tool calls: {tracker.current.tool_calls}")
    
    # Check events
    events = bus.get_events()
    print(f"✓ Telemetry events: {len(events)}")
    
    print()


def demo_logging_api():
    """Demonstrate Logging API"""
    print("LOGGING API DEMONSTRATION")
    print("=" * 50)
    
    from runtime.logging import StructuredLogger, LogLevel, LogContext
    
    logger = StructuredLogger(
        component_name="demo_api",
        console_output=True,
        min_level=LogLevel.INFO
    )
    
    # Basic logging
    logger.info("Info message")
    logger.warning("Warning message")
    
    # Logging with context
    context = LogContext(
        component="demo_api",
        subsystem="test",
        metadata={"test": "value"}
    )
    logger.info("Message with context", context=context)
    
    # Get statistics
    stats = logger.get_statistics()
    print(f"✓ Log entries: {stats['total_entries']}")
    
    print()


def demo_config_api():
    """Demonstrate Configuration API"""
    print("CONFIGURATION API DEMONSTRATION")
    print("=" * 50)
    
    from runtime.config import get_default_config, get_testing_config
    
    # Default config
    default_config = get_default_config()
    print(f"✓ Default config loaded")
    print(f"  Max tokens: {default_config.resources.max_tokens_per_task}")
    print(f"  Log level: {default_config.logging.min_level}")
    
    # Testing config
    testing_config = get_testing_config()
    print(f"✓ Testing config loaded")
    print(f"  Max tokens: {testing_config.resources.max_tokens_per_task}")
    print(f"  Log level: {testing_config.logging.min_level}")
    
    print()


def demo_performance_api():
    """Demonstrate Performance API"""
    print("PERFORMANCE API DEMONSTRATION")
    print("=" * 50)
    
    from runtime.performance import PerformanceMonitor, MetricType
    import time
    
    monitor = PerformanceMonitor("demo_api")
    
    # Record timing
    start = time.time()
    time.sleep(0.1)
    duration = time.time() - start
    monitor.record_timing("test_operation", duration)
    
    # Record custom metric
    monitor.record_custom("custom_metric", 42.0, "units")
    
    # Get statistics
    stats = monitor.get_statistics()
    print(f"✓ Performance metrics: {stats['total_metrics']}")
    print(f"  Timing stats: {stats['timing_stats']}")
    
    print()


def demo_profiler_api():
    """Demonstrate Profiler API"""
    print("PROFILER API DEMONSTRATION")
    print("=" * 50)
    
    from runtime.performance import Profiler
    import time
    
    profiler = Profiler("demo_api")
    
    @profiler.profile_function
    def test_function():
        time.sleep(0.05)
        return "result"
    
    # Execute profiled function
    result = test_function()
    
    # Get statistics
    stats = profiler.get_function_stats("test_function")
    if stats:
        print(f"✓ Function profiled: {stats.function_name}")
        print(f"  Call count: {stats.call_count}")
        print(f"  Average time: {stats.average_time:.4f}s")
    
    print()


def main():
    """Run all API demonstrations"""
    print("=" * 70)
    print("Ω-ABSOLUTE Enhanced Foundation API Demonstrations")
    print("=" * 70)
    print()
    
    demo_core_api()
    demo_governance_api()
    demo_telemetry_api()
    demo_logging_api()
    demo_config_api()
    demo_performance_api()
    demo_profiler_api()
    
    print("=" * 70)
    print("API Demonstrations Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()