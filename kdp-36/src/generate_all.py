#!/usr/bin/env python3
"""Generate all 18 print-ready KDP journal interiors."""

from __future__ import annotations

import sys
import time
import traceback
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from journals.section_a import BUILDERS_A  # noqa: E402
from journals.section_b import BUILDERS_B  # noqa: E402
from journals.section_c import BUILDERS_C  # noqa: E402
from journals.section_d import BUILDERS_D  # noqa: E402


def inspect(path: Path) -> dict:
    r = PdfReader(str(path))
    page = r.pages[0]
    w = float(page.mediabox.width)
    h = float(page.mediabox.height)
    return {
        "file": path.name,
        "pages": len(r.pages),
        "width_in": round(w / 72, 3),
        "height_in": round(h / 72, 3),
        "kb": round(path.stat().st_size / 1024),
    }


def main(only: list[str] | None = None):
    builders = BUILDERS_A + BUILDERS_B + BUILDERS_C + BUILDERS_D
    if only:
        builders = [fn for fn in builders if fn.__name__.split("_")[-1] in only or fn.__name__ in only]
    print(f"Generating {len(builders)} interiors…")
    rows = []
    for fn in builders:
        t0 = time.time()
        try:
            path = fn()
            info = inspect(path)
            info["seconds"] = round(time.time() - t0, 2)
            info["ok"] = True
            print(
                f"  OK  {info['file']:56}  {info['pages']:3}p  "
                f"{info['width_in']}x{info['height_in']}in  {info['kb']}KB  {info['seconds']}s"
            )
            rows.append(info)
        except Exception:
            print(f"  FAIL {fn.__name__}")
            traceback.print_exc()
            rows.append({"file": fn.__name__, "ok": False})
    ok = sum(1 for r in rows if r.get("ok"))
    print(f"\nDone: {ok}/{len(builders)} PDFs")
    return rows


if __name__ == "__main__":
    only = sys.argv[1:] or None
    main(only)
