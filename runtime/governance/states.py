"""
Canonical enumerations for Ω-ABSOLUTE.
References: §7 (Epistemic), §48 (Capability decay), §59 (Source), §61 (Development), §62 (Claim).
"""

from enum import Enum


class DevelopmentState(str, Enum):
    """§61 – Canonical development states. Every component MUST have one of these."""
    NOT_DESIGNED = "NOT_DESIGNED"
    DESIGNED = "DESIGNED"
    SCAFFOLDED = "SCAFFOLDED"
    IMPLEMENTED = "IMPLEMENTED"
    TESTED = "TESTED"
    INTEGRATED = "INTEGRATED"
    BENCHMARKED = "BENCHMARKED"
    VERIFIED = "VERIFIED"
    PROMOTED = "PROMOTED"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"


class ClaimLevel(str, Enum):
    """§62 – Claim discipline. Forbidden to claim higher than what has been achieved."""
    SPECIFICATION = "SPECIFICATION"
    IMPLEMENTATION = "IMPLEMENTATION"
    TEST = "TEST"
    BENCHMARK = "BENCHMARK"
    VERIFICATION = "VERIFICATION"
    DEPLOYMENT = "DEPLOYMENT"
    PRODUCTION = "PRODUCTION"


class CapabilityState(str, Enum):
    """§48 – Capability decay states."""
    ACTIVE = "ACTIVE"
    DEGRADING = "DEGRADING"
    RETEST_REQUIRED = "RETEST_REQUIRED"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    RETIRED = "RETIRED"


class EpistemicState(str, Enum):
    """§7 – Every meaningful proposition MUST have an epistemic state."""
    OBSERVED = "OBSERVED"
    VERIFIED = "VERIFIED"
    SUPPORTED = "SUPPORTED"
    INFERRED = "INFERRED"
    ASSUMED = "ASSUMED"
    HYPOTHESIZED = "HYPOTHESIZED"
    UNKNOWN = "UNKNOWN"
    CONTRADICTED = "CONTRADICTED"
    DISPROVEN = "DISPROVEN"
    STALE = "STALE"


class SourceType(str, Enum):
    """§59 – SOURCE TYPES for provenance."""
    USER_PROVIDED = "USER_PROVIDED"
    PROJECT_FILE = "PROJECT_FILE"
    EXPERIMENT = "EXPERIMENT"
    TOOL = "TOOL"
    WEB_SOURCE = "WEB_SOURCE"
    MODEL_INFERENCE = "MODEL_INFERENCE"
    HYPOTHESIS = "HYPOTHESIS"
