"""
Gap Matrix – AI Reconstruction Protocol §75 STEP 8.
Produces: SPECIFIED / IMPLEMENTED / TESTED / VERIFIED / MISSING / CONFLICTING
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .states import DevelopmentState


class GapStatus(str, Enum):
    SPECIFIED = "SPECIFIED"
    IMPLEMENTED = "IMPLEMENTED"
    TESTED = "TESTED"
    VERIFIED = "VERIFIED"
    MISSING = "MISSING"
    CONFLICTING = "CONFLICTING"


@dataclass
class ComponentGap:
    component_id: str
    canonical_section: str
    specified: bool = True
    development_state: DevelopmentState = DevelopmentState.NOT_DESIGNED
    notes: str = ""
    conflicts: List[str] = field(default_factory=list)

    @property
    def gap_status(self) -> GapStatus:
        if self.conflicts:
            return GapStatus.CONFLICTING
        if not self.specified:
            return GapStatus.MISSING
        mapping = {
            DevelopmentState.NOT_DESIGNED: GapStatus.SPECIFIED,
            DevelopmentState.DESIGNED: GapStatus.SPECIFIED,
            DevelopmentState.SCAFFOLDED: GapStatus.SPECIFIED,
            DevelopmentState.IMPLEMENTED: GapStatus.IMPLEMENTED,
            DevelopmentState.TESTED: GapStatus.TESTED,
            DevelopmentState.INTEGRATED: GapStatus.TESTED,
            DevelopmentState.BENCHMARKED: GapStatus.TESTED,
            DevelopmentState.VERIFIED: GapStatus.VERIFIED,
            DevelopmentState.PROMOTED: GapStatus.VERIFIED,
            DevelopmentState.DEPRECATED: GapStatus.VERIFIED,
            DevelopmentState.RETIRED: GapStatus.VERIFIED,
        }
        return mapping.get(self.development_state, GapStatus.SPECIFIED)


@dataclass
class GapMatrix:
    """Living gap matrix required by reconstruction protocol."""

    components: Dict[str, ComponentGap] = field(default_factory=dict)

    def register(
        self,
        component_id: str,
        canonical_section: str,
        state: DevelopmentState = DevelopmentState.NOT_DESIGNED,
        notes: str = "",
    ) -> None:
        self.components[component_id] = ComponentGap(
            component_id=component_id,
            canonical_section=canonical_section,
            development_state=state,
            notes=notes,
        )

    def update_state(self, component_id: str, state: DevelopmentState) -> None:
        if component_id not in self.components:
            raise KeyError(f"Component '{component_id}' not in gap matrix")
        self.components[component_id].development_state = state

    def add_conflict(self, component_id: str, conflict_note: str) -> None:
        if component_id not in self.components:
            raise KeyError(f"Component '{component_id}' not in gap matrix")
        self.components[component_id].conflicts.append(conflict_note)

    def summary(self) -> Dict[str, int]:
        counts: Dict[str, int] = {s.value: 0 for s in GapStatus}
        for gap in self.components.values():
            counts[gap.gap_status.value] += 1
        return counts

    def to_markdown(self) -> str:
        lines = [
            "# Ω-ABSOLUTE Gap Matrix",
            "",
            "| Component | Section | State | Gap Status | Notes |",
            "|-----------|---------|-------|------------|-------|",
        ]
        for gap in sorted(self.components.values(), key=lambda g: g.component_id):
            notes = gap.notes or ("; ".join(gap.conflicts) if gap.conflicts else "")
            lines.append(
                f"| {gap.component_id} | {gap.canonical_section} | "
                f"{gap.development_state.value} | {gap.gap_status.value} | {notes} |"
            )
        lines.append("")
        lines.append("## Summary")
        for k, v in self.summary().items():
            lines.append(f"- {k}: {v}")
        return "\n".join(lines)
