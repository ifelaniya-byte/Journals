#!/usr/bin/env python3
"""Final QC for release4/ — same rigor as validate_nine.py."""
import re, sys
from pathlib import Path
from pypdf import PdfReader
R = Path(__file__).resolve().parent / "release4"
BLEED = 0.125; CREAM, WHITE = 0.0025, 0.002252
TITLES = {"settle":"SETTLE","middle":"THEMIDDLESEASON","dopamine":"THEDOPAMINEMENU",
          "slow":"THESLOWPAGE","soft":"THE75SOFTJOURNAL","cozy":"COZYCORNERS",
          "botanical":"BOTANICALINK","celestial":"CELESTIALATLAS","tidal":"TIDALINK"}
SPEC = {"settle":(172,(6,9),"cream"),"middle":(160,(6,9),"white"),"dopamine":(150,(6,9),"cream"),
        "slow":(144,(6,9),"cream"),"soft":(96,(6,9),"cream"),"cozy":(104,(8.5,11),"white"),
        "botanical":(104,(8.5,11),"white"),"celestial":(104,(8.5,11),"white"),"tidal":(104,(8.5,11),"white")}
COLORING = ("cozy","botanical","celestial","tidal")
SPOTS = [("settle",4,"TODAY'SSETTLE"),("settle",9,"PRACTICECARD"),("settle",19,"REGULATIONREVIEW"),
         ("middle",4,"DAILYLOG·DAY1"),("middle",31,"MONTH1·REVIEW"),
         ("dopamine",4,"BUILDYOURMENU"),("dopamine",145,"MYMENU"),
         ("slow",4,"SEASONGATE"),("slow",4,"SPRING"),
         ("soft",4,"THESIXRULES"),("soft",12,"WEEK1·RECAP"),("soft",94,"DAY76"),
         ("cozy",2,"HOWTOUSETHISBOOK"),("celestial",2,"HOWTOUSETHISBOOK"),("tidal",2,"HOWTOUSETHISBOOK")]
sq = lambda t: re.sub(r"\s+","",t or "").upper()
fails = []
print(f"{'PRODUCT':11} {'PG':>4} {'TRIM':>8} {'TITLE':>5} {'EMBD':>5} {'BACKS':>5} {'WRAP dims':>20} {'BARC':>4} {'SPINE':>9} {'META':>4}")
for key,(np_,(tw,th),paper) in SPEC.items():
    d = R/key
    rd = PdfReader(str(d/f"{key}_interior.pdf")); mb = rd.pages[0].mediabox
    w,hh = float(mb.width)/72, float(mb.height)/72
    emb = b"/FontFile2" in (d/f"{key}_interior.pdf").read_bytes()
    t1 = TITLES[key] in sq(rd.pages[0].extract_text())
    backs = True
    if key in COLORING:
        backs = not [i+1 for i in range(5,len(rd.pages)-2,2) if sq(rd.pages[i].extract_text())]
    wr = PdfReader(str(d/f"{key}_cover_wrap.pdf")); mw = wr.pages[0].mediabox
    ww, wh = float(mw.width)/72, float(mw.height)/72
    ppi = WHITE if paper=="white" else CREAM; spine = np_*ppi
    ew, eh = 2*BLEED+2*tw+spine, 2*BLEED+th
    txt = wr.pages[0].get_contents().get_data().decode("latin-1")
    barc = bool(re.search(r"1 1 1 rg[\s\S]{0,60}?[-\d.]+ [-\d.]+ 144 86\.4 re f", txt))
    rot = "0 -1 1 0" in txt; exp_spine = spine > 0.35
    md = (d/"metadata.txt").read_text()
    kw = [k for k in re.search(r"KEYWORDS:(.*)", md).group(1).split(",") if k.strip()]
    meta_ok = all(f in md for f in ("TITLE:","SUBTITLE:","AUTHOR:","FORMAT:","PRICE:","CATEGORIES:","KEYWORDS:","DESCRIPTION:")) and len(kw)==7
    ok = (len(rd.pages)==np_ and abs(w-tw)<.01 and abs(hh-th)<.01 and t1 and emb and backs
          and len(wr.pages)==1 and abs(ww-ew)<.01 and abs(wh-eh)<.01 and barc and rot==exp_spine and meta_ok)
    if not ok: fails.append(key)
    print(f"{key:11} {len(rd.pages):>4} {w}x{hh}".ljust(20) + f" {'OK' if t1 else 'NO':>7}{'OK' if emb else 'NO':>6}"
          f"{'OK' if backs else 'NO':>6} {ww:.3f}x{wh:.3f} {'OK' if barc else 'NO':>5} {'yes' if rot else 'no'}/{'y' if exp_spine else 'n':<3}"
          f"{'OK' if meta_ok else 'NO':>6}  {'VALID' if ok else 'FAIL'}")
print()
bad_spots = []
for key, pg, token in SPOTS:
    txt = sq(PdfReader(str(R/key/f"{key}_interior.pdf")).pages[pg].extract_text())
    if token not in txt: bad_spots.append((key, pg+1, token))
print("spot checks:", "ALL OK" if not bad_spots else f"FAILED: {bad_spots}")
fails += [f"spot{b[0]}" for b in bad_spots]
cl = (R/"UPLOAD_CHECKLIST_BATCH4.md").read_text()
n_sec = len(re.findall(r"^## ", cl, re.M))
print(f"checklist sections: {n_sec}/9")
if n_sec != 9: fails.append("checklist")
if fails: print(f"FAILURES: {fails}"); sys.exit(1)
print("\nALL 9 BATCH-4 PRODUCTS: PERFECT")
