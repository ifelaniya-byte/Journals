from pathlib import Path

import pytest

from omega.stationary import Stationary


def test_stationary_does_not_write(tmp_path):
    judge = Stationary(tmp_path)
    target = tmp_path / "secret_fix.py"
    with pytest.raises(RuntimeError, match="must not write"):
        judge.forbid_write(target)
    assert judge.writes == 0
    assert not target.exists()


def test_directive_rework_on_contradiction():
    judge = Stationary(Path("."))
    obs = judge.observe(
        {"claims": {"files": ["x"]}, "facts": {"files": ["y"]}}
    )
    assert obs["contradictions"]
    assert judge.directive(obs, attempts=1, max_attempts=3) == "REWORK"
    assert judge.directive(obs, attempts=3, max_attempts=3) == "ESCALATE"
