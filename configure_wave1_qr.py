#!/usr/bin/env python3
"""Prepare and, after live verification, stamp Wave 1 optional-audio QR codes.

This tool refuses to put a QR code into a print PDF unless all six reviewed audio
assets exist and the real buyer-controlled redirect URLs respond successfully.
It only modifies the six Wave 1 interior PDFs and regenerated actual-page samples.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
REL = ROOT / "release"
QRROOT = ROOT / "qr-routing"
SITE = QRROOT / "site"
CONFIG = ROOT / "brand_config.json"
WAVE1 = [
    ("A01", "dose-and-breathe", "Dose & Breathe", "arrive", "A01-arrive.mp3"),
    ("A04", "softer-words", "Softer Words", "soften", "A04-soften.mp3"),
    ("A05", "night-harbor", "Night Harbor", "harbor", "A05-harbor.mp3"),
    ("B10", "rest-and-regulate", "Rest & Regulate", "settle", "B10-settle.mp3"),
    ("B12", "back-to-enough", "Back to Enough", "enough", "B12-enough.mp3"),
    ("B18", "enough-money-enough-calm", "Enough Money, Enough Calm", "clarity", "B18-clarity.mp3"),
]
COLORS = {
    "A01": "20313D", "A04": "49354A", "A05": "172338",
    "B10": "294A52", "B12": "35443A", "B18": "443C2B",
}
ACCENTS = {
    "A01": "A4C3B2", "A04": "E3B4A5", "A05": "C8CEE8",
    "B10": "A7D2D0", "B12": "D8B887", "B18": "E6C778",
}
TRANSCRIPTS = {
    "A01": "Begin where you are. There is nothing to solve in this minute. Let the page hold one observation, one question, or no words at all. If something belongs with your care team, you can simply write the question down for later. Choose a natural breath if that feels comfortable, or skip it. This is a small private pause, and you may use it in your own way.",
    "A04": "Take a moment before you begin. You do not have to make today sound better than it was. Notice one thing that felt hard, one thing that helped, or one sentence you would offer someone you care about. The page is not asking for a perfect answer. A few honest words, or a blank space, can be enough.",
    "A05": "Let the day become smaller for a moment. You might name one thing you are setting down, one comfort you can choose, or one thought that can wait until tomorrow. There is no correct way to end a day. Stay with the page only as long as it helps, and make the next small choice that feels kind.",
    "B10": "Find a position that feels workable for you. You may notice the room, the support beneath you, or one ordinary sound. If a natural breath feels comfortable, let it come and go without trying to change it. If it does not, simply keep reading or return to the page. This practice is optional, adaptable, and yours to leave at any time.",
    "B12": "You do not need to finish everything before you can begin. Look for one task that can become smaller, one thing that can wait, or one request for support you might make. The next step does not have to be impressive to count. Let this page help you choose what is possible right now, then stop when you have enough.",
    "B18": "Before making a money decision, make room for one small pause. You might write what you know, what you are feeling, and what question still needs a qualified answer. This page does not need you to solve everything today. Choose one manageable next step, or simply give yourself time before reacting.",
}


def valid_domain(value: str) -> str:
    value = value.strip().lower().removeprefix("https://").removeprefix("http://").strip("/")
    if not re.fullmatch(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}", value):
        raise argparse.ArgumentTypeError("use an actual domain only, for example stillworkstudio.com")
    if value.endswith((".example", ".invalid", ".test", ".localhost")):
        raise argparse.ArgumentTypeError("placeholder and local domains cannot be printed")
    return value


def rgb(hex_value: str):
    hex_value = hex_value.lstrip("#")
    return tuple(int(hex_value[i:i+2], 16) / 255 for i in (0, 2, 4))


def write_site(domain: str) -> dict:
    """Make the deterministic route map and mobile-first static listening pages."""
    origin = f"https://www.{domain}"
    redirect_host = f"go.{domain}"
    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / "audio").mkdir(exist_ok=True)
    routes = []
    for ident, slug, title, route, audio in WAVE1:
        destination = f"{origin}/listen/{route}/"
        routes.append({
            "id": ident, "product": title, "route": route, "print_url": f"https://{redirect_host}/{route}",
            "destination": destination, "audio_file": audio, "transcript": TRANSCRIPTS[ident],
        })
        folder = SITE / "listen" / route
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>{html.escape(title)} — optional audio pause</title><meta name=\"robots\" content=\"noindex,nofollow\"><style>
:root{{--ink:#{COLORS[ident]};--accent:#{ACCENTS[ident]};--paper:#f8f5ef}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:#202020;font:18px/1.55 system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif}}main{{max-width:38rem;margin:auto;padding:3rem 1.4rem 4rem}}.eyebrow{{color:var(--ink);font-weight:700;letter-spacing:.08em;font-size:.72rem;text-transform:uppercase}}h1{{font-family:Georgia,serif;font-size:2.1rem;line-height:1.1;margin:.5rem 0 1rem;color:var(--ink)}}.card{{border:1px solid var(--accent);border-radius:1rem;background:white;padding:1.2rem;margin:1.5rem 0}}audio{{width:100%;margin:.5rem 0 1rem}}small{{display:block;color:#555}}.privacy{{font-size:.8rem;color:#555;margin-top:1.5rem}}a{{color:var(--ink)}}</style></head>
<body><main><p class=\"eyebrow\">The Ritual Library · Stillwork Studio</p><h1>{html.escape(title)}</h1><p>This optional audio pause accompanies the paperback. Use it only if it feels useful; it does not replace professional care or advice.</p><section class=\"card\"><audio controls preload=\"metadata\"><source src=\"/audio/{audio}\" type=\"audio/mpeg\">Your browser does not support audio playback.</audio><small>Transcript</small><p>{html.escape(TRANSCRIPTS[ident])}</p></section><p class=\"privacy\">Privacy: this page has no third-party advertising trackers or health-data form. If route measurement is enabled, it is limited to aggregate, non-identifying counts.</p><p><a href=\"/\">The Ritual Library listening room</a></p></main></body></html>
""", encoding="utf-8")
    (SITE / "index.html").write_text("""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>The Ritual Library listening room</title><style>body{max-width:42rem;margin:auto;padding:3rem 1.4rem;font:18px/1.5 system-ui;background:#f8f5ef;color:#20313d}a{color:#20313d}</style></head><body><h1>The Ritual Library listening room</h1><p>Optional short audio pauses that accompany select books.</p><ul>""" + "".join(f'<li><a href="/listen/{r["route"]}/">{html.escape(r["product"])}</a></li>' for r in routes) + "</ul></body></html>", encoding="utf-8")
    payload = {"domain": domain, "redirect_host": redirect_host, "landing_origin": origin, "routes": routes}
    (QRROOT / "routes.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    config.update({"domain": domain, "qr_redirect_host": redirect_host, "landing_origin": origin, "updated": "2026-08-28"})
    CONFIG.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return payload


def make_qr(url: str, path: Path) -> None:
    try:
        import qrcode
        from qrcode.constants import ERROR_CORRECT_H
    except ImportError as err:
        raise SystemExit("Missing qrcode dependency. Run: pip install -r requirements.txt") from err
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=16, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    image.save(path)


def require_live(url: str, expected: str) -> None:
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": "RitualLibraryQRVerifier/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            final = response.url.rstrip("/") + "/"
            wanted = expected.rstrip("/") + "/"
            if response.status != 200 or final != wanted:
                raise SystemExit(f"LIVE CHECK FAILED: {url} ended at {response.status} {response.url}; expected {expected}")
    except urllib.error.URLError as exc:
        raise SystemExit(f"LIVE CHECK FAILED: {url}: {exc}") from exc


def stamp_pdf(pdf_path: Path, ident: str, imprint: str, route: dict, png_path: Path) -> None:
    doc = fitz.open(pdf_path)
    # Title page: replace the old bracketed imprint at the existing visual location.
    page = doc[0]
    page.add_redact_annot(fitz.Rect(105, 420, 328, 455), fill=rgb(COLORS[ident]))
    page.apply_redactions()
    page.insert_textbox(fitz.Rect(75, 430, 358, 448), imprint, fontsize=8.5, fontname="helv", color=(1, 1, 1), align=1, overlay=True)
    # Copyright / note page: remove source placeholders and use the existing blank lower field.
    page = doc[1]
    page.add_redact_annot(fitz.Rect(34, 215, 398, 540), fill=(1, 1, 1))
    page.apply_redactions()
    dark = (0.31, 0.31, 0.31)
    page.insert_text((40, 233), f"Copyright © 2026 {imprint}. All rights reserved.", fontsize=7.2, fontname="helv", color=dark, overlay=True)
    page.insert_text((40, 248), "This edition includes an optional audio pause.", fontsize=7.0, fontname="helv", color=dark, overlay=True)
    page.insert_textbox(fitz.Rect(40, 300, 238, 353), "A quiet optional pause\nScan with your phone camera\nor visit the printed address.", fontsize=7.5, fontname="helv", color=dark, overlay=True)
    page.insert_image(fitz.Rect(259, 292, 342, 375), filename=str(png_path), keep_proportion=True, overlay=True)
    page.insert_textbox(fitz.Rect(230, 383, 373, 401), route["print_url"].replace("https://", ""), fontsize=5.6, fontname="helv", color=dark, align=1, overlay=True)
    # Save compactly and regenerate exactly the actual-page listing samples altered by the stamp.
    tmp = pdf_path.with_suffix(".tmp.pdf")
    doc.save(tmp, garbage=4, deflate=True)
    doc.close()
    tmp.replace(pdf_path)
    doc = fitz.open(pdf_path)
    for number, page_index in ((2, 0), (3, max(1, len(doc) // 12))):
        pix = doc[page_index].get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
        pix.save(str(pdf_path.parent / f"listing_{number:02d}_interior.jpg"))
    doc.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", required=True, type=valid_domain, help="registered buyer-controlled domain, e.g. example.com")
    parser.add_argument("--prepare", action="store_true", help="write static landing pages and route configuration; does not touch print PDFs")
    parser.add_argument("--apply", action="store_true", help="stamp verified QR codes into the six Wave 1 interiors")
    parser.add_argument("--verify-live", action="store_true", help="require every redirect to resolve to the expected live first-party landing page")
    args = parser.parse_args()
    if not args.prepare and not args.apply:
        parser.error("choose --prepare and/or --apply")
    if args.verify_live and not args.apply:
        parser.error("--verify-live is meaningful only with --apply")
    payload = write_site(args.domain)
    print(f"Prepared six static listening pages for {payload['landing_origin']}.")
    if not args.apply:
        print("No print PDFs changed. Add approved MP3s, deploy, and run --apply --verify-live only after routes are live.")
        return
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    imprint = config.get("imprint", "").strip()
    if not imprint:
        raise SystemExit("brand_config.json has no imprint")
    missing_audio = [route["audio_file"] for route in payload["routes"] if not (SITE / "audio" / route["audio_file"]).is_file()]
    if missing_audio:
        raise SystemExit("QR STAMP BLOCKED: final reviewed audio files are missing: " + ", ".join(missing_audio))
    assets = QRROOT / "assets"
    assets.mkdir(exist_ok=True)
    for route in payload["routes"]:
        qr_path = assets / f"{route['id']}-{route['route']}.png"
        make_qr(route["print_url"], qr_path)
        if args.verify_live:
            require_live(route["print_url"], route["destination"])
        ident, slug, _, _, _ = next(item for item in WAVE1 if item[0] == route["id"])
        interior = REL / f"{ident}-{slug}" / "interior.pdf"
        if not interior.is_file():
            raise SystemExit(f"Missing Wave 1 interior: {interior}")
        stamp_pdf(interior, ident, imprint, route, qr_path)
        print(f"Stamped {ident}: {route['print_url']}")
    print("Wave 1 QR stamp complete. Run validator, claims audit, and physical-proof scans; this does not authorize upload.")


if __name__ == "__main__":
    main()
