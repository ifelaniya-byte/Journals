# Ω-ABSOLUTE Enhanced Foundation API Documentation

## Overview

The enhanced Ω-ABSOLUTE foundation provides a comprehensive API for governance, telemetry, logging, configuration, and performance monitoring. This document describes the main interfaces and their usage.

## Core API

### OmegaCore

The immutable governance kernel that enforces safety boundaries and resource ceilings.

```python
from runtime.core.omega_core import OmegaCore, CoreViolationError

# Initialize the core
core = OmegaCore()

# Access immutable properties
identity = core.identity  # "Ω-ABSOLUTE"
formal_name = core.formal_name  # "Bounded Self-Synthesizing Causal Intelligence"
version = core.core_version

# Check resource usage
try:
    core.check_resource("max_tokens_per_task", 100)  # Returns True if within limit
except CoreViolationError as e:
    print(f"Resource violation: {e.violation_type}")
    print(f"Context: {e.context}")

# Enforce safety boundaries
try:
    core.assert_boundary("no_unrestricted_self_modification")
except CoreViolationError as e:
    print(f"Boundary violation: {e}")

# Promote components (requires full evidence)
evidence = {
    "UNIT_TEST": True,
    "ABLATION": True,
    "ADVERSARIAL": True,
    "REGRESSION": True,
    "RESOURCE": True,
    "REPRODUCTION": True,
    "TRANSFER": True,
}
core.promote_component("component_id", evidence)

# Access governance systems
claim_discipline = core.claim_discipline
gap_matrix = core.gap_matrix
```

### MetaController

The meta-controller makes decisions about task execution and safety.

```python
from runtime.core.meta_controller import MetaController, ControllerDecision

meta = MetaController(core)

# Make safety decisions
decision = meta.decide({
    "irreversible": False,
    "authorized": True
})

if decision.kind == ControllerDecision.ALLOW:
    print("Action allowed")
elif decision.kind == ControllerDecision.REJECT_UNSAFE:
    print("Action rejected as unsafe")

# Check meta-controller status
status = meta.status()
```

## Governance API

### ClaimDiscipline

Enforces that components cannot claim higher status than their actual development state.

```python
from runtime.governance.claim_discipline import ClaimDiscipline, ClaimViolationError
from runtime.governance.states import DevelopmentState, ClaimLevel

disc = ClaimDiscipline()

# Register component state
disc.register("component_id", DevelopmentState.IMPLEMENTED)

# Check if claim is allowed
try:
    disc.assert_claim_allowed("component_id", ClaimLevel.VERIFICATION)
except ClaimViolationError as e:
    print(f"Claim violation: {e.component_id}")
    print(f"Claimed: {e.claimed_level}, Actual: {e.actual_state}")

# Get safe status string
status = disc.safe_status_string("component_id")
```

### GapMatrix

Tracks implementation gaps across all components.

```python
from runtime.governance.gap_matrix import GapMatrix, GapStatus

matrix = GapMatrix()

# Register component
matrix.register("component_id", "§X Section", DevelopmentState.IMPLEMENTED)

# Update state
matrix.update_state("component_id", DevelopmentState.VERIFIED)

# Get summary
summary = matrix.summary()
print(f"IMPLEMENTED: {summary['IMPLEMENTED']}")
print(f"VERIFIED: {summary['VERIFIED']}")

# Export to markdown
markdown = matrix.to_markdown()
```

### ChangeControlRecord

Tracks all architectural changes with approval workflow.

```python
from runtime.governance.change_control import ChangeControlRecord, ChangeStatus

record = ChangeControlRecord(
    author_or_agent="developer",
    previous_version="0.1.0",
    new_version="0.1.1",
    reason="Enhancement",
    expected_gain="Better performance",
    expected_risk="Low",
    test_plan="Unit tests",
    rollback_plan="Git revert"
)

# Lifecycle
record.approve()  # ChangeStatus.APPROVED
record.apply()    # ChangeStatus.APPLIED
record.rollback() # ChangeStatus.ROLLED_BACK
record.reject("Testing failed")  # ChangeStatus.REJECTED
```

## Telemetry API

### ResourceTracker

Tracks resource usage and enforces Core ceilings.

```python
from runtime.telemetry.tracker import ResourceTracker, TelemetryBus
from runtime.telemetry.events import ResourceUsage

bus = TelemetryBus()
tracker = ResourceTracker(core, bus)

# Record resource usage
tracker.record(
    ResourceUsage(tokens=100, tool_calls=5, wall_time_seconds=10),
    subsystem="test",
    action="operation"
)

# Access current usage
current = tracker.current
print(f"Tokens: {current.tokens}")
print(f"Tool calls: {current.tool_calls}")

# Get snapshot
snapshot = tracker.snapshot()

# Access telemetry events
events = bus.get_events(subsystem="test")
```

### TelemetryEvent

Structured event for telemetry data.

```python
from runtime.telemetry.events import TelemetryEvent, ResourceUsage

event = TelemetryEvent(
    subsystem="component_name",
    action="operation_name",
    resource_usage=ResourceUsage(tokens=100)
)

# Convert to dictionary
event_dict = event.to_dict()
```

## Logging API

### StructuredLogger

Provides structured logging with context awareness.

```python
from runtime.logging import StructuredLogger, LogLevel, LogContext

# Create logger
logger = StructuredLogger(
    component_name="my_component",
    log_file=Path("logs/my_component.log"),
    console_output=True,
    min_level=LogLevel.INFO
)

# Basic logging
logger.info("Operation completed")
logger.warning("Resource usage high")
logger.error("Operation failed")

# Logging with context
context = LogContext(
    component="my_component",
    subsystem="processing",
    task_id="task_123",
    metadata={"user": "alice"}
)
logger.info("Processing started", context=context, input_size=1000)

# Retrieve entries
recent_entries = logger.get_entries(limit=10)
error_entries = logger.get_entries(level=LogLevel.ERROR)

# Get statistics
stats = logger.get_statistics()
print(f"Total entries: {stats['total_entries']}")

# Export to JSON
logger.export_json("logs/export.json")
```

### LoggingIntegration

Utilities for integrating logging with other components.

```python
from runtime.logging import LoggingIntegration

# Create component logger
logger = LoggingIntegration.create_component_logger(
    component_name="my_component",
    log_dir=Path("logs"),
    enable_console=True
)

# Integrate with telemetry
LoggingIntegration.integrate_with_telemetry(logger, telemetry_bus)
```

## Configuration API

### ConfigManager

Manages configuration loading and validation.

```python
from runtime.config import ConfigManager, ConfigLoadError

# Load configuration from file
config_manager = ConfigManager(Path("config.yaml"))
try:
    config = config_manager.load()
except ConfigLoadError as e:
    print(f"Config error: {e}")

# Access configuration
max_tokens = config.resources.max_tokens_per_task
log_level = config.logging.min_level

# Save configuration
config_manager.save(Path("config_backup.yaml"), format="yaml")

# Reload configuration
config = config_manager.reload()
```

### OmegaConfig

Main configuration dataclass.

```python
from runtime.config import OmegaConfig, ResourceConfig, LoggingConfig

# Create custom configuration
config = OmegaConfig(
    resources=ResourceConfig(
        max_tokens_per_task=2_000_000,
        max_wall_time_seconds=7200
    ),
    logging=LoggingConfig(
        min_level="DEBUG",
        file_output=True
    )
)

# Convert to dictionary
config_dict = config.to_dict()
```

### Default Configurations

Pre-configured configurations for different environments.

```python
from runtime.config import get_default_config, get_production_config, get_testing_config

# Default configuration
default_config = get_default_config()

# Production configuration
production_config = get_production_config()

# Testing configuration
testing_config = get_testing_config()
```

## Performance API

### PerformanceMonitor

Tracks timing, memory, and custom performance metrics.

```python
from runtime.performance import PerformanceMonitor, MetricType

monitor = PerformanceMonitor("my_component")

# Record metrics
monitor.record_timing("operation", 0.5, metadata={"input_size": 100})
monitor.record_memory("data_structure", 150.5)
monitor.record_custom("custom_metric", 42.0, "units")

# Context managers
with monitor.measure_time("expensive_operation"):
    # do expensive operation
    pass

with monitor.measure_memory("memory_intensive"):
    # do memory intensive operation
    pass

# Manual timing
monitor.start_timing("manual_operation")
# do operation
duration = monitor.stop_timing("manual_operation")

# Retrieve metrics
timing_metrics = monitor.get_metrics(metric_type=MetricType.TIMING)
all_metrics = monitor.get_metrics(limit=100)

# Get statistics
stats = monitor.get_statistics()
print(f"Average time: {stats['timing_stats']['average']}")

# Get slowest operations
slowest = monitor.get_slowest_operations(limit=5)

# Export metrics
monitor.export_json("performance_metrics.json")
```

### Profiler

Function-level profiling with decorators.

```python
from runtime.performance import Profiler

profiler = Profiler("my_component")

# Profile function
@profiler.profile_function
def my_function():
    # code
    pass

# Profile with memory tracking
@profiler.profile_function_with_memory
def memory_intensive_function():
    # code
    pass

# Get function statistics
stats = profiler.get_function_stats("my_function")
print(f"Average time: {stats.average_time}")
print(f"Call count: {stats.call_count}")

# Get all statistics
all_stats = profiler.get_all_stats()

# Get slowest functions
slowest = profiler.get_slowest_functions(limit=10)

# Reset profiling data
profiler.reset()
```

## CLI API

### Enhanced CLI Interface

Command-line interface for foundation management.

```bash
# Display comprehensive status
python cli.py status

# Run tests
python cli.py test
python cli.py test --verbose

# Inspect components
python cli.py inspect                    # List all components
python cli.py inspect omega.core         # Inspect specific component

# Run solve demo
python cli.py solve "test task description"

# Test resource tracking
python cli.py resource-test

# Demonstrate logging
python cli.py logging-demo
```

## Public API

### solve()

Main entry point for task solving (currently foundation stub).

```python
from runtime import solve

result = solve({
    "description": "task description"
})

# Result structure
{
    "status": "FOUNDATION_ONLY",
    "answer": None,
    "architecture_used": "foundation_stub",
    "claim_discipline_note": "...",
    "meta_decision": {...},
    "core": {
        "identity": "Ω-ABSOLUTE",
        "core_version": "0.1.0-foundation",
        ...
    }
}
```

### get_core()

Get the singleton OmegaCore instance.

```python
from runtime import get_core

core = get_core()
```

### get_meta_controller()

Get the singleton MetaController instance.

```python
from runtime import get_meta_controller

meta = get_meta_controller()
```

## Error Handling

### CoreViolationError

Raised when Core safety boundaries are violated.

```python
try:
    core.check_resource("max_tokens_per_task", 2_000_000)
except CoreViolationError as e:
    print(f"Violation type: {e.violation_type}")
    print(f"Context: {e.context}")
    print(f"Full error: {e.to_dict()}")
```

### ClaimViolationError

Raised when claim discipline is violated.

```python
try:
    disc.assert_claim_allowed("component", ClaimLevel.VERIFICATION)
except ClaimViolationError as e:
    print(f"Component: {e.component_id}")
    print(f"Claimed: {e.claimed_level}")
    print(f"Actual: {e.actual_state}")
    print(f"Full error: {e.to_dict()}")
```

### ConfigLoadError

Raised when configuration cannot be loaded.

```python
try:
    config = config_manager.load()
except ConfigLoadError as e:
    print(f"File: {e.file_path}")
    print(f"Details: {e.details}")
```

## Development States

Canonical development states for components:

```python
from runtime.governance.states import DevelopmentState

states = [
    DevelopmentState.NOT_DESIGNED,
    DevelopmentState.DESIGNED,
    DevelopmentState.SCAFFOLDED,
    DevelopmentState.IMPLEMENTED,
    DevelopmentState.TESTED,
    DevelopmentState.INTEGRATED,
    DevelopmentState.BENCHMARKED,
    DevelopmentState.VERIFIED,
    DevelopmentState.PROMOTED,
    DevelopmentState.DEPRECATED,
    DevelopmentState.RETIRED,
]
```

## Claim Levels

Levels of claims that can be made about components:

```python
from runtime.governance.states import ClaimLevel

levels = [
    ClaimLevel.SPECIFICATION,
    ClaimLevel.IMPLEMENTATION,
    ClaimLevel.TEST,
    ClaimLevel.BENCHMARK,
    ClaimLevel.VERIFICATION,
    ClaimLevel.PRODUCTION,
    ClaimLevel.DEPLOYMENT,
]
```

## Integration Examples

### Complete Foundation Workflow

```python
from runtime import get_core, get_meta_controller, solve
from runtime.logging import LoggingIntegration
from runtime.performance import PerformanceMonitor
from runtime.config import get_default_config

# Initialize components
core = get_core()
meta = get_meta_controller()
config = get_default_config()

# Setup logging
logger = LoggingIntegration.create_core_logger(
    component_name="omega_core",
    log_dir=Path("logs")
)

# Setup performance monitoring
monitor = PerformanceMonitor("omega_core")

# Execute task with monitoring
with monitor.measure_time("task_execution"):
    result = solve({"description": "test task"})

# Log results
logger.info("Task completed", result=result)

# Check performance
stats = monitor.get_statistics()
print(f"Execution time: {stats['timing_stats']['total']}")
```

### Custom Component with Full Integration

```python
from runtime.core.omega_core import OmegaCore
from runtime.logging import StructuredLogger, LogContext
from runtime.performance import Profiler
from runtime.config import ConfigManager

class CustomComponent:
    def __init__(self, config_path):
        self.core = OmegaCore()
        self.config = ConfigManager(config_path).load()
        self.logger = StructuredLogger("custom_component")
        self.profiler = Profiler("custom_component")
    
    @profiler.profile_function_with_memory
    def process(self, data):
        context = LogContext(
            component="custom_component",
            task_id="processing_task"
        )
        
        self.logger.info("Starting processing", context=context)
        
        # Processing logic
        result = self._process_data(data)
        
        self.logger.info("Processing completed", context=context)
        return result
    
    def _process_data(self, data):
        # Actual processing implementation
        return data
```

## Best Practices

1. **Always use claim discipline** - Register components and enforce claim levels
2. **Monitor resources** - Use ResourceTracker for all operations
3. **Log structured events** - Use StructuredLogger with context
4. **Profile performance** - Use PerformanceMonitor for critical paths
5. **Validate configuration** - Always validate loaded configuration
6. **Handle errors gracefully** - Use specific exception types
7. **Use context managers** - Leverage timing/memory context managers
8. **Export metrics** - Regularly export performance and telemetry data
9. **Test governance** - Verify claim discipline and resource limits
10. **Document changes** - Use ChangeControlRecord for all modifications

## Version Information

- **Core Version**: 0.1.0-foundation  
- **Spec Version**: 1.0-frozen  
- **API Version**: 1.0-enhanced  

## Support

For issues or questions about the enhanced foundation API, refer to:
- Foundation Analysis (FOUNDATION-ANALYSIS.md)
- Implementation Plan (2-DAY-IMPLEMENTATION-PLAN.md)
- Main README (README.md)