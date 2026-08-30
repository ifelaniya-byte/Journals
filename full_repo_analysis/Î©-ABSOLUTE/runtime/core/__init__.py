"""
Immutable Ω Core – §4.
The following MUST NOT be silently self-modifiable:
identity, safety boundaries, audit requirements, promotion requirements,
rollback mechanisms, resource ceilings, irreversible-action policies,
verification hierarchy, provenance requirements, truthfulness requirements,
change logging.
"""

from .omega_core import OmegaCore, CoreViolationError
from .version import CORE_VERSION, PROJECT_VERSION

__all__ = [
    "OmegaCore",
    "CoreViolationError",
    "CORE_VERSION",
    "PROJECT_VERSION",
]
