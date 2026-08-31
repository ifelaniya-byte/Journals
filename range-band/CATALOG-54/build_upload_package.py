#!/usr/bin/env python3
"""Build the complete 54-SKU upload package (candidate-only, no upload).
Reads frozen catalogs under /tmp; writes runbook + field CSV + entry sheet.
"""
from __future__ import annotations
import csv, json, re
from pathlib import Path

Q = Path("/tmp/qmp-adhd")
R = Path("/tmp/Journals-remote/range-band")
OUT = Path("/home/user")

def fld(t: str, n: str) -> str:
    m = re.search(rf"(?m)^\s*{re.escape(n)}[^\n]*\n(.+)$", t)
    return m.group(1).strip() if m else ""

def kws(t: str) -> list[str]:
    m = re.search(r"SEVEN BACKEND KEYWORDS\n(.*?)(?=\n\s*\n|\n[A-Z][A-Z /(]+\n)", t, re.I | re.S)
    return [k.strip() for k in re.findall(r"(?m)^\s*\d+\.\s*(.+?)\s*$", m.group(1))] if m else []

def cats_block(t: str) -> list[str]:
    m = re.search(r"CATEGORIES / BISAC\n(.*?)(?=\nSEVEN BACKEND KEYWORDS)", t, re.S)
    return [l.strip() for l in m.group(1).strip().split("\n") if l.strip()] if m else []

QM_WAVE = {"dopamine":1,"soft":2,"middle":3,"cozy":4}
RB_WAVE = {1:1,5:2,9:3,30:4,10:5,12:6}
QM_WAVE_ALL = {s:1 for s in QM_WAVE}
RB_WAVE_ALL = {n:(1 if n in RB_WAVE else 2 if n in {2,19,8,25,7,24,22} else 3 if n in {3,6,23,27,20,11,15,18} else 4) for n in range(1,37)}

def qm_blocks():
    inv = {r["id"]: r for r in csv.DictReader(open(OUT/"products_inventory.csv", encoding="utf-8"))}
    rows = list(csv.DictReader(open(Q/"CATALOG.csv", encoding="utf-8")))
    out=[]
    for r in rows:
        n=int(r["n"]); slug=r["interior_file"].split("/")[0]
        batch=r["batch"]; rel=f"release{'3' if batch=='B3' else '4'}/{slug}"
        t=(Q/rel/"metadata.txt").read_text(encoding="utf-8")
        d=inv[f"QM-{n:02d}"]
        dprice = f"${float(d['digital_price']):.2f}" if str(d['digital_price']).replace('.','').isdigit() else "print-only"
        actual_interior=f"{slug}_interior.pdf" if (Q/rel/f"{slug}_interior.pdf").exists() else "?"
        out.append({
            "id": f"QM-{n:02d}", "imprint":"Quiet Mind Press", "wave": QM_WAVE_ALL.get(slug,2),
            "order": QM_WAVE.get(slug, 99), "title": fld(t,"AMAZON TITLE"), "subtitle": fld(t,"SUBTITLE"),
            "author":"Quiet Mind Press","series": fld(t,"SERIES"),"trim": fld(t,"TRIM"),
            "pages": fld(t,"PAGE COUNT"), "paper": re.search(r"Paper:\s*([a-zA-Z]+)", fld(t,"INTERIOR")).group(1) if re.search(r"Paper:\s*([a-zA-Z]+)", fld(t,"INTERIOR")) else "?",
            "cats": fld(t,"CATEGORIES"), "keywords": kws(t), "price":"$9.99",
            "interior_file": rel+"/"+actual_interior, "cover_file": rel+f"/{slug}_cover_wrap.pdf",
            "images":"cover.jpg + listing_02-05_interior.jpg + listing_06_callout.jpg + listing_07_series.jpg",
            "copy": rel+"/metadata.txt", "bn": d["bn_status"], "digital": dprice,
            "hc": d["hc_status"], "rank": d["rank"], "notes": d["notes"],
        })
    return out

def rb_blocks():
    inv = {r["id"]: r for r in csv.DictReader(open(OUT/"products_inventory.csv", encoding="utf-8"))}
    rows = list(csv.DictReader(open(R/"KDP-Complete-Kit/METADATA.csv", encoding="utf-8")))
    out=[]
    for r in rows:
        n=int(r["n"])
        real=next(p for p in (R/"KDP-Complete-Kit").iterdir() if p.is_dir() and p.name.startswith(f"{n:02d}_"))
        t=(real/"listing.txt").read_text(encoding="utf-8")
        d=inv[f"RB-{n:02d}"]
        out.append({
            "id": f"RB-{n:02d}", "imprint":"Range Band Press", "wave": RB_WAVE_ALL[n],
            "order": RB_WAVE.get(n, 99), "title": fld(t,"TITLE"), "subtitle": fld(t,"SUBTITLE"),
            "author":"Range Band Press","series": r["series"], "trim": fld(t,"TRIM"),
            "pages": fld(t,"PAGE COUNT"), "paper":"white",
            "cats":" | ".join(cats_block(t)), "keywords": kws(t), "price":"$9.99",
            "interior_file": real.name+"/"+next(p.name for p in real.glob("*_interior.pdf")),
            "cover_file": real.name+"/"+next(p.name for p in real.glob("*COVER_WRAP.pdf")),
            "images":"none (listing images not built for RB)",
            "copy": real.name+"/listing.txt", "bn":"LIST", "digital":"$9.99", "hc":"not built",
            "rank": d["rank"], "notes": d["notes"],
        })
    return out

def main():
    qm=qm_blocks(); rb=rb_blocks(); allp=sorted(qm+rb, key=lambda x:(x["imprint"], x["order"], x["id"]))
    # CSV
    f=OUT/"UPLOAD_FIELDS_ALL54.csv"
    with open(f,"w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh, fieldnames=["id","imprint","wave","order","title","subtitle","author","series","trim","pages","paper","cats","keywords","price","interior_file","cover_file","images","copy","bn","digital","hc","rank","notes"])
        w.writeheader()
        for p in allp: w.writerow(p)
    # Entry sheet (all blocks)
    L=["# KDP entry sheet — all 54 products (paste-ready, human gate)","",
       "Read-only. No upload performed. Every field below comes from the frozen catalog trees:",
       "`ADHD-Journals` @ `3feca69` · `Range-Band` @ `8562469`.","",
       "**Global:** $9.99 · bleed OFF · black & white · English · ED OFF · author/imprint per line ·",
       "upload the WRAP as cover (never COVER_FRONT) · create the 6 series pages first.","",
       "QM copy = paste AMAZON TITLE from metadata.txt (not the short cover word).",
       "RB copy = paste HTML from listing.txt (title + subtitle + keywords).",""]
    L.append("## Quiet Mind Press — 18"); L.append("")
    for p in qm:
        L.append(f"### {p['id']} · {p['title']}")
        L.append(f"- **Subtitle:** {p['subtitle']}")
        L.append(f"- **Author / series:** Quiet Mind Press · {p['series']}")
        L.append(f"- **Trim / pages / paper:** {p['trim']} · {p['pages']} pp · {p['paper']}")
        L.append(f"- **Interior / cover file:** `{p['interior_file']}` · `{p['cover_file']}`")
        L.append(f"- **Categories:** {p['cats']}")
        L.append(f"- **Keywords (7):** {' · '.join(p['keywords'])}")
        L.append(f"- **Price:** $9.99 · ED OFF · **Images:** {p['images']}")
        L.append(f"- **Copy:** `{p['copy']}` · **B&N:** {p['bn']} · **Digital:** {p['digital']} · **HC:** {p['hc']} · **Rank:** {p['rank']}")
        L.append("")
    L.append("## Range Band Press — 36"); L.append("")
    for p in rb:
        L.append(f"### {p['id']} · {p['title']}")
        L.append(f"- **Subtitle:** {p['subtitle']}")
        L.append(f"- **Author / series:** Range Band Press · {p['series']}")
        L.append(f"- **Trim / pages / paper:** {p['trim']} · {p['pages']} pp · white · B&W · bleed OFF")
        L.append(f"- **Interior / cover file (ACTUAL):** `{p['interior_file']}` · `{p['cover_file']}`")
        L.append(f"- **Categories:** {p['cats']}")
        L.append(f"- **Keywords (7):** {' · '.join(p['keywords'])}")
        L.append(f"- **Price:** $9.99 · ED OFF · **Images:** {p['images']}")
        L.append(f"- **Copy:** `{p['copy']}` · **Digital:** $9.99 · **B&N:** LIST · **Rank:** {p['rank']}")
        L.append("")
    L.append("> All 6 RB Wave-1 listing files reference a stale interior filename; upload the actual `*_interior.pdf` path shown above (frozen files not renamed).")
    L.append("> Empty QR boxes: RB 03, 09, 17 (paste URL later only). Spine OFF: RB 07.")
    (OUT/"UPLOAD_ENTRY_SHEET_ALL54.md").write_text("\n".join(L),encoding="utf-8")
    # Runbook
    L=["# Upload runbook — 54 SKUs to KDP paperback ($9.99)","",
       "Prepared 2026-08-31 · read-only · **no upload performed** · sources: frozen `ADHD-Journals` @ `3feca69` + `Range-Band` @ `8562469`","",
       "## Who does what","",
       "| Step | Who |",
       "|---|---|",
       "| Prepare fields/files | ✅ done (this package) |",
       "| Create 6 series pages | human (KDP) |",
       "| Upload each KDP product | **human** — logged-in Amazon/KDP account, browser + TOS; no agent path exists and policy blocks `kdp_upload` |",
       "| Verify live listing, price, ED | human (then feed back data to agent) |",
       "| Run ads | human; agent drafts only; no ads on RB-14 |","",
       "## Sequence (per SELL_HUB — do not skip, do not all-at-once for ads)","",
       f"**Wave 1 (10, upload now):** QM dopamine, soft, middle, cozy → RB 01, 09, 05, 30, 10, 12.",
       "**Wave 2+ cadence:** QM ≈5 titles/week after clean Wave-1 data; RB Wave 2 (7: 02,19,08,25,07,24,22) → Wave 3 (8) → Wave 4 (15).",
       "**Channels order:** KDP paperback (all 54) → Wave 2 digital (QM 17 + RB 36) → QM hardcovers (7) + Blurb (6) → B&N (QM 11 thick; RB 36) → Lulu → Ingram (after ISBNs).",
       "**Never:** ads-blast all 54; mix series; $14.99 on KDP; ED ON; digital-PDF Middle Season; list RB-14 with ads.","",
       "## Global KDP settings (every product)","",
       "| Setting | Value |",
       "|---|---|",
       "| Price | $9.99 |",
       "| Bleed | OFF | Interior: black & white | Language: English |",
       "| Expanded Distribution | OFF | Author: imprint name | ISBN: KDP free fine |",
       "| Cover | **WRAP** PDF (never COVER_FRONT / merged) |",
       "| QM title | paste AMAZON TITLE from metadata.txt | RB title | KDP title from listing.txt |",
       "| Series | one of the 6 pages | |","",
       "## Series pages (create first)","",
       "- Quiet Mind Journals (8) · Quiet Mind Color (10) · GLP-1 Tracking (9) · Wellness Tracking (9) · GLP-1 Companion (9) · Wellness Companion (9)","",
       "## Per-title fields","",
       "Full paste-ready fields for all 54: `UPLOAD_ENTRY_SHEET_ALL54.md` (human-readable) and `UPLOAD_FIELDS_ALL54.csv` (machine).","",
       "## Per-product notes","",
       "- **RB interior filenames:** listing.txt/METADATA reference stale names; upload the actual `*_interior.pdf` listed in the sheet. Verified page counts match.",
       "- **RB listing images:** none built (36). Conversion will be cover-only on Amazon. Recommend generating interior spread JPGs before ads on Wave 1 (offer available).",
       "- **QM Middle Season:** print-only — do not upload a digital PDF.",
       "- **QM B&N:** list 11 ≥120pp only; hold thin 7 (firststroke, garden, soft, cozy, botanical, celestial, tidal).",
       "- **QM hardcovers:** 7 journals LIST; 10 coloring HOLD; Night none (5×8 trim).",
       "- **Empty QR:** RB 03, 09, 17 — no URL invented. **Spine OFF:** RB 07.",
       "- **RB-14:** KDP listing allowed but ADS HOLD (vs Middle Season).",
       "- **Proof before ads (RB):** 01 (6×9), 07 (5×8), 09 (8.5×11).",
       "","## Human gate checklist",
       "- [ ] Create 6 series pages",
       "- [ ] Upload Wave 1 (10) in order $9.99 / bleed OFF / ED OFF / WRAP",
       "- [ ] Confirm live listings + prices",
       "- [ ] Wave 2+ per cadence; ads only Wave 1 until ~10 reviews",
       "- [ ] Never mix imprints or series; never $14.99 on KDP",
       ""]
    (OUT/"UPLOAD_RUNBOOK_54.md").write_text("\n".join(L),encoding="utf-8")
    print("wrote UPLOAD_RUNBOOK_54.md, UPLOAD_ENTRY_SHEET_ALL54.md, UPLOAD_FIELDS_ALL54.csv")
    print("blocks:", len(qm), "QM +", len(rb), "RB")

main()
