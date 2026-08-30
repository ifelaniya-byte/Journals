"""Omega reflective loop: retrieve → math → research → brainstorm → plan → act → critique → revise."""

from __future__ import annotations

import json
from typing import Any, Callable

STAGES = (
    "retrieve",
    "math",
    "research",
    "brainstorm",
    "plan",
    "act",
    "critique",
    "revise",
)


def _rank(mission: dict[str, Any]) -> dict[str, Any]:
    risk = {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(
        str(mission.get("risk", "medium")), 2
    )
    priority = int(mission.get("priority") or 0)
    pages = 0
    try:
        pages = int(mission.get("pages") or 0)
    except Exception:
        pages = 0
    score = priority * 10 + risk * 3 + min(pages, 200) / 50
    return {"risk_weight": risk, "priority": priority, "score": round(score, 3)}


def run_loop(
    mission: dict[str, Any],
    atlas: dict[str, Any],
    previous_failures: list,
    actor_fn: Callable[[str], dict[str, Any]],
    apply_fn: Callable[[dict[str, Any]], list[str]],
    ledger_fn: Callable[[str, Any], None],
) -> dict[str, Any]:
    trace: list[dict[str, Any]] = []

    retrieve = {
        "mission_id": mission.get("mission_id"),
        "atlas_files": len(atlas.get("files") or []),
        "failures": previous_failures,
    }
    ledger_fn("retrieve", retrieve)
    trace.append({"stage": "retrieve", "data": retrieve})

    math = _rank(mission)
    ledger_fn("math", math)
    trace.append({"stage": "math", "data": math})

    research = {
        "dependencies": atlas.get("dependencies"),
        "tests": atlas.get("tests"),
        "fingerprint": atlas.get("fingerprint"),
    }
    ledger_fn("research", research)
    trace.append({"stage": "research", "data": research})

    brainstorm = {
        "options": [
            "draft in generated/ only",
            "refuse blocked actions",
            "keep imprint and price faithful",
        ]
    }
    ledger_fn("brainstorm", brainstorm)
    trace.append({"stage": "brainstorm", "data": brainstorm})

    plan = {
        "steps": [
            "actor drafts JSON/copy",
            "writes land in generated/",
            "dual verify",
            "dual oversee",
        ]
    }
    ledger_fn("plan", plan)
    trace.append({"stage": "plan", "data": plan})

    prompt = (
        "You are the experimental merged/combined/evolved actor.\n"
        "Work only the mission. Return JSON.\n"
        "MISSION_JSON:"
        + json.dumps(
            {
                "title": mission.get("title"),
                "requirements": mission.get("requirements") or [],
                "output_path": mission.get("output_path") or "generated/asset.json",
                "action": mission.get("action") or "draft_copy",
                "mock_body": mission.get("mock_body"),
            }
        )
        + "\nATLAS_FINGERPRINT:"
        + str(atlas.get("fingerprint"))
        + "\nFAILURES:"
        + json.dumps(previous_failures)
    )
    actor_result = actor_fn(prompt)
    changed = apply_fn(actor_result)
    actor_result.setdefault("implementation", {})["applied"] = changed
    ledger_fn("act", {"changed": changed, "requested": actor_result.get("requested_verdict")})
    trace.append({"stage": "act", "data": {"changed": changed}})

    critique = {
        "claimed_files": (actor_result.get("implementation") or {}).get("files_changed"),
        "applied": changed,
        "mismatch": set(
            (actor_result.get("implementation") or {}).get("files_changed") or []
        )
        != set(changed),
    }
    ledger_fn("critique", critique)
    trace.append({"stage": "critique", "data": critique})

    revise = {"needed": bool(previous_failures) or bool(critique["mismatch"])}
    ledger_fn("revise", revise)
    trace.append({"stage": "revise", "data": revise})

    return {"trace": trace, "actor_result": actor_result, "changed": changed, "math": math}
