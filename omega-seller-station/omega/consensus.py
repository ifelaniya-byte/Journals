from __future__ import annotations

from typing import Any


def reconcile(scan_a: dict[str, Any], scan_b: dict[str, Any]) -> dict[str, Any]:
    """Map reconciliation after both scans exist. Disagreements are first-class."""
    files_a = {f["path"] for f in scan_a.get("files", [])}
    files_b = {f["path"] for f in scan_b.get("files", [])}
    only_a = sorted(files_a - files_b)
    only_b = sorted(files_b - files_a)
    secrets = sorted(
        set(scan_a.get("secrets_suspects", [])) | set(scan_b.get("secrets_suspects", []))
    )
    destructive = sorted(
        set(scan_a.get("destructive_suspects", []))
        | set(scan_b.get("destructive_suspects", []))
    )
    disagreements = []
    if only_a:
        disagreements.append({"kind": "files_only_A", "paths": only_a})
    if only_b:
        disagreements.append({"kind": "files_only_B", "paths": only_b})
    if scan_a.get("file_count") != scan_b.get("file_count"):
        disagreements.append(
            {
                "kind": "count",
                "A": scan_a.get("file_count"),
                "B": scan_b.get("file_count"),
            }
        )
    return {
        "files": sorted(files_a | files_b),
        "file_count": len(files_a | files_b),
        "secrets_suspects": secrets,
        "destructive_suspects": destructive,
        "todos": sorted(set(scan_a.get("todos", [])) | set(scan_b.get("todos", []))),
        "ci": sorted(set(scan_a.get("ci", [])) | set(scan_b.get("ci", []))),
        "containers": sorted(
            set(scan_a.get("containers", [])) | set(scan_b.get("containers", []))
        ),
        "dependencies": sorted(
            set(scan_a.get("dependencies", [])) | set(scan_b.get("dependencies", []))
        ),
        "disagreements": disagreements,
        "independent": True,
    }
