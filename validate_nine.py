import re, zlib
from pathlib import Path
from pypdf import PdfReader
from reportlab.lib.units import inch

R = Path("/home/user/release3")
BLEED = 0.125
CREAM, WHITE = 0.0025, 0.002252

SPEC = {  # key: (dir, pages, trim_in, paper, squash_title)
 "dump":        ("dump",200,(5.5,8.5),"cream","THE5-MINUTEDUMP"),
 "parallel":    ("parallel",160,(7,10),"cream","PARALLELLIVES"),
 "night":       ("night",120,(5,8),"cream","THENIGHTPAGES"),
 "firststroke": ("firststroke",100,(8.5,11),"white","FIRSTSTROKES"),
 "garden":      ("garden",100,(8.5,11),"white","EASYGARDEN"),
 "mosaic":      ("mosaic",120,(8.5,11),"white","MOSAICMIND"),
 "woodland":    ("woodland",120,(8.5,11),"white","WOODLANDWONDERS"),
 "fractal":     ("fractal",140,(8.5,11),"white","FRACTALDREAMS"),
 "architect":   ("architect",140,(8.5,11),"white","ARCHITECTURALVISIONS"),
}

def squash(t): return re.sub(r"\s+","",t or "").upper()
fails = []
print(f"{'PRODUCT':13} {'PG':>4} {'TRIM':>12} {'TITLE':>6} {'EMBED':>6}  RESULT")
for key,(d,npages,(tw,th),paper,title) in SPEC.items():
    ip = R/d/f"{d}_interior.pdf"
    rd = PdfReader(str(ip))
    n = len(rd.pages)
    mb = rd.pages[0].mediabox
    w_in, h_in = float(mb.width)/72, float(mb.height)/72
    t1 = squash(rd.pages[0].extract_text())
    embedded = b"/FontFile2" in ip.read_bytes()[:200000] or b"/FontFile2" in ip.read_bytes()
    ok = (n==npages) and abs(w_in-tw)<0.01 and abs(h_in-th)<0.01 and (title in t1) and embedded
    if not ok:
        fails.append(key)
        detail=[]
        if n!=npages: detail.append(f"pages {n}!={npages}")
        if abs(w_in-tw)>=0.01 or abs(h_in-th)>=0.01: detail.append(f"trim {w_in:.2f}x{h_in:.2f}")
        if title not in t1: detail.append(f"title missing p1")
        if not embedded: detail.append("fonts not embedded")
        print(f"{key:13} {n:>4} {w_in:.2f}x{h_in:.2f} {'OK' if title in t1 else 'NO':>6} {'OK' if embedded else 'NO':>6}  FAIL: {', '.join(detail)}")
    else:
        print(f"{key:13} {n:>4} {w_in:.2f}x{h_in:.2f} {'OK':>6} {'OK':>6}  VALID")

print()
print("COVER WRAPS")
for key,(d,npages,(tw,th),paper,title) in SPEC.items():
    wp = R/d/f"{d}_cover_wrap.pdf"
    rd = PdfReader(str(wp))
    n = len(rd.pages)
    mb = rd.pages[0].mediabox
    w_in, h_in = float(mb.width)/72, float(mb.height)/72
    ppi = WHITE if paper=="white" else CREAM
    spine = npages*ppi
    ew = 2*BLEED + 2*tw + spine
    eh = 2*BLEED + th
    # barcode: white fill + rect in content stream
    data = wp.read_bytes()
    found_barcode = False
    for m in re.finditer(rb"stream\r?\n", data):
        s = m.end()
        e = data.find(b"endstream", s)
        raw = data[s:e]
        try: txt = zlib.decompress(raw).decode("latin-1")
        except Exception: continue
        if re.search(r"1 1 1 rg[\s\S]{0,120}?[\d.]+ [\d.]+ [\d.]+ [\d.]+ re\s*f", txt):
            found_barcode = True; break
    ok = n==1 and abs(w_in-ew)<0.01 and abs(h_in-eh)<0.01 and found_barcode
    if not ok: fails.append(key+"_wrap")
    size_ok = "OK" if abs(w_in-ew)<0.01 and abs(h_in-eh)<0.01 else "SIZEFAIL"
    print(f"{key:13} pages={n} {w_in:.3f}x{h_in:.3f}in (exp {ew:.3f}x{eh:.3f}) barcode={'OK' if found_barcode else 'MISSING'} -> {'VALID' if ok else 'FAIL'}")

print()
print("BLANK-BACK CHECK (coloring books: even pages in art section must have no text)")
for key in ("firststroke","garden","mosaic","woodland","fractal","architect"):
    d = SPEC[key][0]
    rd = PdfReader(str(R/d/f"{d}_interior.pdf"))
    bad = [i+1 for i in range(5, len(rd.pages)-2, 2) if squash(rd.pages[i].extract_text())]
    print(f"{key:13} {'OK — all art backs blank' if not bad else 'NON-BLANK: '+str(bad[:5])}")

print()
print("SPOT TEXT CHECKS")
checks = [("dump", 4, "HOWTOUSETHISBOOK"), ("parallel", 14, "REFLECTION"), ("night", 12, "BODYSCAN"),
          ("mosaic", 5, "MOSAICMIND")]
for key, pg, token in checks:
    d = SPEC[key][0]
    rd = PdfReader(str(R/d/f"{d}_interior.pdf"))
    txt = squash(rd.pages[pg].extract_text())
    print(f"{key:13} p{pg+1} contains {token}: {'OK' if token in txt else 'NO'}")

print()
print("ALL NINE PRODUCTS VALID" if not fails else f"FAILURES: {fails}")
