from __future__ import annotations

import re
import subprocess
from pathlib import Path

from .shadow import IGNORED_DIRS

SECRET_PATTERNS: list[tuple[str, str]] = [
    ("aws_access_key", r"AKIA[0-9A-Z]{16}"),
    ("private_key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("github_token", r"gh[pousr]_[A-Za-z0-9]{36,}"),
    ("openai_style_key", r"sk-[A-Za-z0-9]{32,}"),
    ("google_api_key", r"AIza[0-9A-Za-z_-]{35}"),
]
DESTRUCTIVE_PATTERNS: list[tuple[str, str]] = [
    ("pipe_to_shell", r"curl[^|\n]*\|\s*(ba)?sh"),
    ("wipe_fs", r"mkfs(\.\w+)?\b"),
    ("fork_bomb", r":\(\)\s*\{\s*:\|:\s*&\s*\}\s*;"),
    ("rm_root", r"rm\s+-[^\n]*r[^\n]*f[^\n]*/(\s|$)"),
]
TODO_RE = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")

DEP_FILES = (
    "requirements.txt", "pyproject.toml", "setup.py", "Pipfile",
    "package.json", "Cargo.toml", "go.mod", "pom.xml", "Gemfile",
)
TEXT_SUFFIXES = {
    ".py", ".sh", ".bash", ".zsh", ".js", ".ts", ".jsx", ".tsx", ".java",
    ".rb", ".go", ".rs", ".c", ".h", ".cpp", ".hpp", ".cs", ".php",
    ".sql", ".yml", ".yaml", ".toml", ".json", ".ini", ".cfg", ".conf",
    ".env", ".md", ".txt", ".mk",
}
PLAIN_NAMES = {"Dockerfile", "Makefile", "LICENSE", ".gitignore", ".env"}
MAX_SCAN_BYTES = 2_000_000


def _is_text_name(name: str) -> bool:
    if name in PLAIN_NAMES:
        return True
    return Path(name).suffix in TEXT_SUFFIXES


def _content_findings(rel: str, text: str) -> list[dict]:
    findings: list[dict] = []
    for name, pat in SECRET_PATTERNS:
        if re.search(pat, text):
            findings.append({
                "key": f"secret.{name}",
                "value": {"file": rel, "pattern": pat},
            })
    for name, pat in DESTRUCTIVE_PATTERNS:
        if re.search(pat, text):
            findings.append({
                "key": f"destructive.{name}",
                "value": {"file": rel, "pattern": pat},
            })
    n = len(TODO_RE.findall(text))
    if n:
        findings.append({"key": "todo.count",
                         "value": {"file": rel, "count": n}})
    return findings


def _todo_top(counts: dict[str, int]) -> dict | None:
    if not counts:
        return None
    file = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return {"file": file, "count": counts[file]}


def scan_filesystem(root: Path) -> dict:
    """Scan A: filesystem truth. Walks the tree directly."""
    root = Path(root)
    inventory: set[str] = set()
    findings: list[dict] = []
    todo_counts: dict[str, int] = {}
    dep_files, test_files, ci_files, containers = [], [], [], []

    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        r = rel.as_posix()
        inventory.add(r)
        base = rel.name.lower()
        if base in {d.lower() for d in DEP_FILES}:
            dep_files.append(r)
        if "test" in base.lower() or rel.parts[0].lower() in {"tests", "test"}:
            test_files.append(r)
        if rel.parts[0] == ".github" and "workflows" in rel.parts:
            ci_files.append(r)
        if base.startswith("dockerfile") or base.startswith("docker-compose"):
            containers.append(r)
        if _is_text_name(base):
            try:
                if p.stat().st_size > MAX_SCAN_BYTES:
                    continue
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for fd in _content_findings(r, text):
                if fd["key"] == "todo.count":
                    todo_counts[r] = fd["value"]["count"]
                else:
                    findings.append(fd)

    top = _todo_top(todo_counts)
    if top:
        findings.append({"key": "todo.top", "value": top})
    findings.append({"key": "python.project",
                     "value": any(f.endswith(".py") for f in inventory)})
    findings.append({"key": "deps.manifest", "value": sorted(dep_files)})
    findings.append({"key": "tests.present", "value": bool(test_files)})
    findings.append({"key": "ci.present", "value": bool(ci_files)})
    findings.append({"key": "containers.present", "value": bool(containers)})
    return {"method": "filesystem", "inventory": inventory,
            "findings": findings}


def scan_git(root: Path) -> dict:
    """Scan B: git-index truth. Reads file content from the index
    (git cat-file), NOT from the working tree - a different evidence
    source by construction, so the two scans can genuinely disagree
    (untracked files, unstaged edits)."""
    root = Path(root)

    def git(*args: str) -> str:
        try:
            r = subprocess.run(
                ["git", *args], cwd=root, text=True,
                capture_output=True, timeout=30,
            )
            return r.stdout if r.returncode == 0 else ""
        except Exception:
            return ""

    tracked = {l.strip() for l in git("ls-files").splitlines() if l.strip()}
    if not tracked:
        fs = scan_filesystem(root)
        fs["method"] = "filesystem-fallback(no-git)"
        return fs

    findings: list[dict] = []
    todo_counts: dict[str, int] = {}
    for f in sorted(tracked):
        if any(part in IGNORED_DIRS for part in Path(f).parts):
            continue
        if not _is_text_name(Path(f).name):
            continue
        blob = git("cat-file", "-p", f":{f}")
        if not blob:
            continue
        if len(blob) > MAX_SCAN_BYTES:
            continue
        for fd in _content_findings(f, blob):
            if fd["key"] == "todo.count":
                todo_counts[f] = fd["value"]["count"]
            else:
                findings.append(fd)
    top = _todo_top(todo_counts)
    if top:
        findings.append({"key": "todo.top", "value": top})

    dirty = git("status", "--short").splitlines()
    findings.append({"key": "git.dirty", "value": bool(dirty)})
    branch = git("branch", "--show-current").strip()
    findings.append({"key": "git.branch", "value": branch or "(detached)"})
    dep = [f for f in tracked
           if Path(f).name.lower() in {d.lower() for d in DEP_FILES}]
    findings.append({"key": "deps.manifest", "value": sorted(dep)})
    findings.append({"key": "tests.present",
                     "value": any("test" in f.lower() for f in tracked)})
    findings.append({"key": "ci.present",
                     "value": any(f.startswith(".github/workflows")
                                  for f in tracked)})
    findings.append({"key": "python.project",
                     "value": any(f.endswith(".py") for f in tracked)})
    return {"method": "git-index", "inventory": set(tracked),
            "findings": findings}


def reconcile(a: dict, b: dict) -> dict:
    """Consensus map. Both scans must independently agree; disagreements
    are surfaced, never silently resolved."""
    confirmed, single, disputed = [], [], []
    by_key_a: dict[str, list[dict]] = {}
    by_key_b: dict[str, list[dict]] = {}
    for f in a["findings"]:
        by_key_a.setdefault(f["key"], []).append(f["value"])
    for f in b["findings"]:
        by_key_b.setdefault(f["key"], []).append(f["value"])

    def _unwrap(v):
        # single-finding keys carry the scalar/dict directly;
        # only genuinely multi-valued keys stay lists
        if isinstance(v, list) and len(v) == 1:
            return v[0]
        return v

    for key in sorted(set(by_key_a) | set(by_key_b)):
        va, vb = by_key_a.get(key), by_key_b.get(key)
        if va is not None and vb is not None:
            if va == vb:
                confirmed.append({"key": key, "value": _unwrap(va)})
            else:
                disputed.append({"key": key, "a": va, "b": vb})
        else:
            single.append({"key": key, "value": _unwrap(va or vb),
                           "source": "a" if va else "b"})

    inv_both = a["inventory"] & b["inventory"]
    return {
        "scan_a_method": a["method"],
        "scan_b_method": b["method"],
        "confirmed": confirmed,
        "single_source": single,
        "disputed": disputed,
        "inventory": {
            "both": len(inv_both),
            "a_only": sorted(a["inventory"] - b["inventory"])[:50],
            "b_only": sorted(b["inventory"] - a["inventory"])[:50],
        },
    }
