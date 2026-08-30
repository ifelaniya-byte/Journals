#!/usr/bin/env python3
"""
Ω-ABSOLUTE Enhanced CLI Interface
Provides command-line tools for foundation testing, inspection, and management.
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Optional

# Add runtime to path
sys.path.insert(0, str(Path(__file__).parent))

from runtime import get_core, get_meta_controller, solve
from runtime.governance.states import DevelopmentState
from runtime.logging import StructuredLogger, LogLevel, LogContext, LoggingIntegration
from runtime.telemetry.tracker import TelemetryBus, ResourceTracker
from runtime.telemetry.events import ResourceUsage


class OmegaCLI:
    """Command-line interface for Ω-ABSOLUTE foundation"""
    
    def __init__(self):
        self.core = get_core()
        self.meta = get_meta_controller()
        self.logger = LoggingIntegration.create_core_logger(enable_console=False)
    
    def status(self) -> None:
        """Display comprehensive foundation status"""
        print("=" * 70)
        print(f"  {self.core.identity}")
        print(f"  {self.core.formal_name}")
        print(f"  Core version : {self.core.core_version}")
        print(f"  Project version: {self.core.project_version}")
        print(f"  Spec version : {self.core.spec_version}")
        print("=" * 70)
        print()
        
        print("Meta-Controller Status:")
        for k, v in self.meta.status().items():
            print(f"  {k}: {v}")
        print()
        
        print("Gap Matrix Summary:")
        for k, v in self.core.gap_matrix.summary().items():
            print(f"  {k}: {v}")
        print()
        
        print("Safety Boundaries:")
        for b in sorted(self.core.safety_boundaries, key=lambda x: x.name):
            status = "✓" if b.enforceable else "○"
            print(f"  {status} {b.name}: {b.description}")
        print()
        
        print("Resource Ceilings:")
        for name, ceiling in self.core.resource_ceilings.items():
            print(f"  - {name}: {ceiling.limit} {ceiling.unit}")
        print()
        
        print("Promotion Requirements:")
        for i, r in enumerate(sorted(self.core.promotion_requirements), 1):
            print(f"  {i}. {r}")
        print()
        
        print("Verification Hierarchy:")
        for i, stage in enumerate(self.core.verification_hierarchy, 1):
            print(f"  {i}. {stage}")
        print()
    
    def test(self, verbose: bool = False) -> None:
        """Run foundation tests"""
        import subprocess
        
        print("Running Ω-ABSOLUTE Foundation Tests...")
        print("=" * 70)
        
        # Run unit tests
        print("\nUnit Tests:")
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/unit", "-v"],
            cwd=Path(__file__).parent,
            capture_output=not verbose,
            text=not verbose
        )
        
        if not verbose:
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
        
        unit_success = result.returncode == 0
        
        # Run integration tests
        print("\nIntegration Tests:")
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/integration", "-v"],
            cwd=Path(__file__).parent,
            capture_output=not verbose,
            text=not verbose
        )
        
        if not verbose:
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
        
        integration_success = result.returncode == 0
        
        print("\n" + "=" * 70)
        if unit_success and integration_success:
            print("✓ All tests passed")
        else:
            print("✗ Some tests failed")
            if not unit_success:
                print("  - Unit tests failed")
            if not integration_success:
                print("  - Integration tests failed")
        
        return unit_success and integration_success
    
    def inspect(self, component: Optional[str] = None) -> None:
        """Inspect foundation components"""
        if component:
            self._inspect_component(component)
        else:
            self._list_components()
    
    def _list_components(self) -> None:
        """List all registered components"""
        print("Registered Components:")
        print("=" * 70)
        
        for component_id in sorted(self.core.gap_matrix.components.keys()):
            state = self.core.gap_matrix.get_state(component_id)
            section = self.core.gap_matrix.get_section(component_id)
            claim_state = self.core.claim_discipline.get_state(component_id)
            
            print(f"\nComponent: {component_id}")
            print(f"  Section: {section}")
            print(f" Gap State: {state.value if state else 'UNKNOWN'}")
            print(f" Claim State: {claim_state.value if claim_state else 'UNKNOWN'}")
            
            # Get safe status string
            status = self.core.claim_discipline.safe_status_string(component_id)
            print(f"  Status: {status}")
    
    def _inspect_component(self, component_id: str) -> None:
        """Inspect specific component"""
        state = self.core.gap_matrix.get_state(component_id)
        section = self.core.gap_matrix.get_section(component_id)
        claim_state = self.core.claim_discipline.get_state(component_id)
        
        if not state and not claim_state:
            print(f"Component '{component_id}' not found")
            return
        
        print(f"Component Inspection: {component_id}")
        print("=" * 70)
        print(f"Section: {section}")
        print(f"Gap Matrix State: {state.value if state else 'UNKNOWN'}")
        print(f"Claim Discipline State: {claim_state.value if claim_state else 'UNKNOWN'}")
        print(f"Safe Status: {self.core.claim_discipline.safe_status_string(component_id)}")
        
        # Check if component can make various claims
        from runtime.governance.states import ClaimLevel
        print("\nClaim Capabilities:")
        for level in ClaimLevel:
            try:
                allowed = self.core.claim_discipline.assert_claim_allowed(
                    component_id, level, raise_on_violation=False
                )
                status = "✓" if allowed else "✗"
                print(f"  {status} {level.value}")
            except Exception:
                print(f"  ✗ {level.value} (error)")
    
    def solve_demo(self, description: str) -> None:
        """Run solve() with demo task"""
        print(f"Running solve() with task: {description}")
        print("=" * 70)
        
        result = solve({"description": description})
        
        print("Result:")
        print(f"  Status: {result['status']}")
        print(f"  Answer: {result['answer']}")
        print(f"  Architecture: {result['architecture_used']}")
        print(f"  Claim Note: {result['claim_discipline_note']}")
        print(f"  Meta Decision: {result['meta_decision']}")
        print(f"  Core Identity: {result['core']['identity']}")
        print(f"  Core Version: {result['core']['core_version']}")
    
    def resource_test(self) -> None:
        """Test resource tracking"""
        print("Resource Tracking Test")
        print("=" * 70)
        
        bus = TelemetryBus()
        tracker = ResourceTracker(self.core, bus)
        
        # Test normal operations
        print("\n1. Normal resource usage:")
        tracker.record(ResourceUsage(tokens=100, tool_calls=2), "test", "operation1")
        print(f"   Tokens: {tracker.current.tokens}")
        print(f"   Tool calls: {tracker.current.tool_calls}")
        
        # Test accumulation
        print("\n2. Resource accumulation:")
        tracker.record(ResourceUsage(tokens=50, tool_calls=1), "test", "operation2")
        print(f"   Tokens: {tracker.current.tokens}")
        print(f"   Tool calls: {tracker.current.tool_calls}")
        
        # Test ceiling enforcement
        print("\n3. Ceiling enforcement:")
        try:
            tracker.record(ResourceUsage(tokens=2_000_000), "test", "overflow")
            print("   ✗ Ceiling enforcement failed")
        except Exception as e:
            print(f"   ✓ Ceiling enforced: {str(e)[:50]}...")
        
        # Test telemetry events
        print("\n4. Telemetry events:")
        events = bus.get_events()
        print(f"   Total events: {len(events)}")
        for event in events:
            print(f"   - {event.subsystem}: {event.action}")
    
    def logging_demo(self) -> None:
        """Demonstrate logging capabilities"""
        print("Structured Logging Demo")
        print("=" * 70)
        
        # Create logger
        logger = StructuredLogger(
            component_name="demo_component",
            console_output=True,
            min_level=LogLevel.DEBUG
        )
        
        # Log at various levels
        print("\n1. Logging at different levels:")
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        
        # Log with context
        print("\n2. Logging with context:")
        context = LogContext(
            component="demo_component",
            subsystem="test_subsystem",
            task_id="task_123",
            metadata={"test": "value"}
        )
        logger.info("Message with context", context=context, extra_data="extra")
        
        # Show statistics
        print("\n3. Logging statistics:")
        stats = logger.get_statistics()
        print(f"   Total entries: {stats['total_entries']}")
        print(f"   Level counts: {stats['level_counts']}")
        
        # Show recent entries
        print("\n4. Recent log entries:")
        recent = logger.get_entries(limit=3)
        for entry in recent:
            print(f"   - {entry.level.value}: {entry.message}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Ω-ABSOLUTE Enhanced CLI Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  status          Display comprehensive foundation status
  test            Run foundation tests
  inspect [comp]  Inspect components (or list all)
  solve <desc>    Run solve() with demo task
  resource-test   Test resource tracking
  logging-demo    Demonstrate logging capabilities
        """
    )
    
    parser.add_argument(
        "command",
        choices=["status", "test", "inspect", "solve", "resource-test", "logging-demo"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "args",
        nargs="*",
        help="Command arguments"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    cli = OmegaCLI()
    
    if args.command == "status":
        cli.status()
    elif args.command == "test":
        success = cli.test(verbose=args.verbose)
        sys.exit(0 if success else 1)
    elif args.command == "inspect":
        component = args.args[0] if args.args else None
        cli.inspect(component)
    elif args.command == "solve":
        description = args.args[0] if args.args else "demo task"
        cli.solve_demo(description)
    elif args.command == "resource-test":
        cli.resource_test()
    elif args.command == "logging-demo":
        cli.logging_demo()


if __name__ == "__main__":
    main()