#!/usr/bin/env python3
"""Independent verification of the Volume 3 kits (read-only)."""
import csv, json, re
from pathlib import Path
from pypdf import PdfReader

ROOT = Path("/home/user/new-catalog")
KIT = ROOT / "KDP-Complete-Kit"
BLACKLIST = re.compile(
    r"\bozempic\b|\bwegovy\b|\bmounjaro\b|\bsaxenda\b|\bzepbound\b|\brybelsus\b"
    r"|\b75\s*hard\b|\btreats nausea\b|\bvagus[- ]nerve stimulation\b|\bpolyvagal exercises\b"
    r"|\belderly coloring book\b", re.I)
CLAIM = re.compile(r"\b(cure[sd]?|diagnos(?:e|is|ing))\b", re.I)
NEG = re.compile(r"\b(not|does not|never|no)\b[^.]{0,70}\b(cure|diagnos)", re.I)
TARGET_TRIM = {(6.0, 9.0), (8.5, 11.0), (5.0, 8.0)}
BLEED = 0.125
SPINE_PER_PAGE = 0.002252


def pdf_info(p):
    r = PdfReader(str(p))
    box = r.pages[0].mediabox
    return len(r.pages), round(float(box.width) / 72, 3), round(float(box.height) / 72, 3)


def text_of(p):
    r = PdfReader(str(p))
    out = []
    for pg in r.pages:
        try:
            out.append(pg.extract_text() or "")
        except Exception:
            out.append("")
    return "\n".join(out)


def main():
    rows = []
    issues = []
    seen = {}
    kw_issues = []
    for folder in sorted(KIT.iterdir()):
        if not folder.is_dir() or not folder.name[:2].isdigit():
            continue
        files = sorted(p.name for p in folder.iterdir())
        listing = folder / "listing.txt"
        interior = next((folder / f for f in files if f.endswith("_interior.pdf")), None)
        wrap = next((folder / f for f in files if "COVER_WRAP" in f), None)
        row = {"n": folder.name[:2], "folder": folder.name, "files": files}
        if len(files) < 4:
            issues.append(f"{row['n']}: expected 4 kit files, got {files}")
        if not listing.exists():
            issues.append(f"{row['n']}: no listing.txt")
            continue
        txt = listing.read_text(encoding="utf-8")
        m = re.search(r"PAGE COUNT\n(\d+)", txt)
        declared = int(m.group(1)) if m else None
        row["declared_pages"] = declared
        m2 = re.search(r"TRIM\n([\d.]+)\" × ([\d.]+)\"", txt)
        dtrim = (float(m2.group(1)), float(m2.group(2))) if m2 else None
        row["declared_trim"] = dtrim
        if interior:
            p, w, h = pdf_info(interior)
            row["interior_pages"] = p
            row["interior_trim"] = (w, h)
            if declared and p != declared:
                issues.append(f"{row['n']}: listing {declared}p != interior {p}p")
            if (w, h) not in TARGET_TRIM:
                issues.append(f"{row['n']}: trim {w}x{h} not in KDP set")
            body = text_of(interior)
            hits = [m.group(0) for m in BLACKLIST.finditer(body.lower())]
            claims = [m.group(0) for m in CLAIM.finditer(body)
                      if not NEG.search(body[max(0, m.start() - 100):m.end() + 100])]
            if hits:
                issues.append(f"{row['n']}: interior blacklist {hits[:3]}")
            if claims:
                issues.append(f"{row['n']}: interior claim words {claims[:3]}")
            row["interior_text_scan"] = "clean"
        else:
            issues.append(f"{row['n']}: no interior PDF")
        if wrap and declared and dtrim:
            wp, ww, wh = pdf_info(wrap)
            spine = round(declared * SPINE_PER_PAGE, 4)
            exp_w = round(2 * BLEED + 2 * dtrim[0] + spine, 3)
            exp_h = round(2 * BLEED + dtrim[1], 3)
            row["wrap_size"] = (ww, wh)
            row["expected_wrap"] = (exp_w, exp_h)
            if abs(ww - exp_w) > 0.02 or abs(wh - exp_h) > 0.02:
                issues.append(f"{row['n']}: wrap {ww}x{wh} vs expected {exp_w}x{exp_h}")
        rows.append(row)
        # keywords
        m = re.search(r"SEVEN BACKEND KEYWORDS\n(.*?)(?=\n\s*\n|\n[A-Z][A-Z /(]+\n)", txt, re.I | re.S)
        if m:
            for k in re.findall(r"(?m)^\s*\d+\.\s*(.+?)\s*$", m.group(1)):
                key = k.lower().strip()
                if key in seen:
                    kw_issues.append((row["n"], key, seen[key]))
                seen[key] = row["n"]
    summary = {
        "kits": len(rows),
        "files_ok": all(len(r["files"]) >= 4 for r in rows),
        "issues": issues,
        "keyword_issues": kw_issues,
        "unique_keywords": len(seen),
        "pages_min": min(r.get("interior_pages", 0) for r in rows),
        "pages_max": max(r.get("interior_pages", 0) for r in rows),
    }
    (ROOT / "VERIFY_VOL3.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k not in ("issues", "keyword_issues")}, indent=2))
    if issues:
        print("ISSUES:", issues)
    if kw_issues:
        print("KW:", kw_issues)
    print("VERIFY:", "PASS" if not issues and not kw_issues else "FAIL")


main()
