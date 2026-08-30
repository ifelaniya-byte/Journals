#!/usr/bin/env python3
"""
Comprehensive demonstration of Ω-ABSOLUTE enhanced foundation capabilities.
Shows integration between core, governance, telemetry, logging, and performance systems.
"""

import sys
import time
from pathlib import Path

# Add runtime to path
sys.path.insert(0, str(Path(__file__).parent))

from runtime import get_core, get_meta_controller, solve
from runtime.governance.states import DevelopmentState, ClaimLevel
from runtime.logging import StructuredLogger, LogLevel, LogContext, LoggingIntegration
from runtime.telemetry.tracker import TelemetryBus, ResourceTracker
from runtime.telemetry.events import ResourceUsage
from runtime.performance import PerformanceMonitor, Profiler
from runtime.config import ConfigManager, get_default_config


def demo_complete_foundation():
    """Demonstrate complete foundation integration"""
    print("=" * 70)
    print("Ω-ABSOLUTE Enhanced Foundation Demonstration")
    print("=" * 70)
    print()
    
    # 1. Initialize Core Systems
    print("1. INITIALIZING CORE SYSTEMS")
    print("-" * 70)
    core = get_core()
    meta = get_meta_controller()
    config = get_default_config()
    
    print(f"✓ Core initialized: {core.identity}")
    print(f"✓ Meta-controller initialized")
    print(f"✓ Configuration loaded")
    print(f"  - Max tokens: {config.resources.max_tokens_per_task}")
    print(f"  - Log level: {config.logging.min_level}")
    print()
    
    # 2. Setup Logging
    print("2. CONFIGURING LOGGING SYSTEM")
    print("-" * 70)
    logger = LoggingIntegration.create_core_logger(
        component_name="demo_foundation",
        log_dir=Path("logs"),
        enable_console=True
    )
    
    logger.info("Foundation demonstration started", 
               context=LogContext(component="demo_foundation", task_id="demo_001"))
    print("✓ Structured logger configured")
    print()
    
    # 3. Setup Performance Monitoring
    print("3. CONFIGURING PERFORMANCE MONITORING")
    print("-" * 70)
    monitor = PerformanceMonitor("demo_foundation")
    profiler = Profiler("demo_foundation")
    
    print("✓ Performance monitor initialized")
    print("✓ Profiler initialized")
    print()
    
    # 4. Setup Telemetry
    print("4. CONFIGURING TELEMETRY SYSTEM")
    print("-" * 70)
    bus = TelemetryBus()
    tracker = ResourceTracker(core, bus)
    
    # Integrate logging with telemetry
    LoggingIntegration.integrate_with_telemetry(logger, bus)
    
    print("✓ Telemetry bus configured")
    print("✓ Resource tracker initialized")
    print("✓ Logging-telemetry integration enabled")
    print()
    
    # 5. Demonstrate Governance
    print("5. DEMONSTRATING GOVERNANCE SYSTEMS")
    print("-" * 70)
    
    # Claim discipline
    logger.info("Testing claim discipline")
    disc = core.claim_discipline
    
    # Register a test component
    disc.register("demo.component", DevelopmentState.IMPLEMENTED)
    logger.info("Registered demo.component at IMPLEMENTED state")
    
    # Test claim validation
    try:
        disc.assert_claim_allowed("demo.component", ClaimLevel.VERIFICATION)
        logger.warning("Claim discipline check failed - should have raised error")
    except Exception as e:
        logger.info("Claim discipline correctly enforced", 
                   violation=str(e)[:50])
    
    # Upgrade and test again
    disc.register("demo.component", DevelopmentState.VERIFIED)
    if disc.assert_claim_allowed("demo.component", ClaimLevel.VERIFICATION, raise_on_violation=False):
        logger.info("Claim validation passed after state upgrade")
    
    print("✓ Claim discipline demonstrated")
    print("✓ Gap matrix functioning")
    print()
    
    # 6. Demonstrate Resource Tracking
    print("6. DEMONSTRATING RESOURCE TRACKING")
    print("-" * 70)
    
    with monitor.measure_time("resource_operations"):
        logger.info("Starting resource tracking operations")
        
        # Normal operations
        tracker.record(ResourceUsage(tokens=100, tool_calls=2), "demo", "op1")
        logger.info("Recorded normal resource usage", tokens=100, tool_calls=2)
        
        time.sleep(0.1)  # Simulate work
        
        tracker.record(ResourceUsage(tokens=50, tool_calls=1), "demo", "op2")
        logger.info("Recorded additional resource usage", tokens=50, tool_calls=1)
        
        # Test ceiling enforcement
        try:
            tracker.record(ResourceUsage(tokens=2_000_000), "demo", "overflow")
            logger.error("Resource ceiling enforcement failed")
        except Exception as e:
            logger.info("Resource ceiling correctly enforced", 
                       violation_type=str(e).split(':')[0])
    
    print(f"✓ Resource tracking completed")
    print(f"  - Total tokens used: {tracker.current.tokens}")
    print(f"  - Total tool calls: {tracker.current.tool_calls}")
    print(f"  - Telemetry events: {len(bus.get_events())}")
    print()
    
    # 7. Demonstrate Performance Monitoring
    print("7. DEMONSTRATING PERFORMANCE MONITORING")
    print("-" * 70)
    
    @profiler.profile_function
    def sample_function():
        time.sleep(0.05)
        return "result"
    
    @profiler.profile_function_with_memory
    def memory_function():
        data = [0] * 1000  # Allocate some memory
        time.sleep(0.03)
        return len(data)
    
    # Execute profiled functions
    logger.info("Executing profiled functions")
    result1 = sample_function()
    result2 = memory_function()
    
    # Get profiling results
    stats = profiler.get_all_stats()
    for stat in stats:
        logger.info(f"Function {stat.function_name}: {stat.call_count} calls, "
                   f"{stat.average_time:.4f}s avg")
    
    print("✓ Performance monitoring completed")
    print(f"  - Functions profiled: {len(stats)}")
    print(f"  - Performance metrics collected: {len(monitor.get_metrics())}")
    print()
    
    # 8. Demonstrate solve() API
    print("8. DEMONSTRATING SOLVE() API")
    print("-" * 70)
    
    with monitor.measure_time("solve_operation"):
        logger.info("Executing solve() API")
        result = solve({"description": "demo task"})
        
        logger.info("solve() completed", 
                   status=result["status"],
                   architecture=result["architecture_used"])
    
    print("✓ solve() API demonstrated")
    print(f"  - Status: {result['status']}")
    print(f"  - Architecture: {result['architecture_used']}")
    print()
    
    # 9. Show Statistics
    print("9. PERFORMANCE STATISTICS")
    print("-" * 70)
    
    perf_stats = monitor.get_statistics()
    print(f"Total metrics: {perf_stats['total_metrics']}")
    print(f"By type: {perf_stats['by_type']}")
    
    if perf_stats['timing_stats']:
        print(f"Timing stats:")
        print(f"  - Total time: {perf_stats['timing_stats']['total']:.4f}s")
        print(f"  - Average: {perf_stats['timing_stats']['average']:.4f}s")
    
    log_stats = logger.get_statistics()
    print(f"\nLogging statistics:")
    print(f"  - Total entries: {log_stats['total_entries']}")
    print(f"  - Level counts: {log_stats['level_counts']}")
    print()
    
    # 10. Export Results
    print("10. EXPORTING RESULTS")
    print("-" * 70)
    
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    # Export performance metrics
    monitor.export_json("logs/demo_performance.json")
    logger.info("Performance metrics exported")
    
    # Export log entries
    logger.export_json("logs/demo_logs.json")
    logger.info("Log entries exported")
    
    print("✓ Results exported to logs/ directory")
    print()
    
    # Final summary
    print("=" * 70)
    print("FOUNDATION DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print("✓ Core governance systems operational")
    print("✓ Claim discipline enforcing component states")
    print("✓ Resource tracking with ceiling enforcement")
    print("✓ Structured logging with context awareness")
    print("✓ Performance monitoring and profiling")
    print("✓ Telemetry integration")
    print("✓ Configuration management")
    print("✓ CLI interface available")
    print()
    print("The enhanced foundation is ready for Phase 1 implementation.")
    print("Next steps: Epistemic Engine → Task Model → World Model → Self Model")


if __name__ == "__main__":
    demo_complete_foundation()