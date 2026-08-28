# Wave 1 QR + audio release gate

**Decision date:** August 28, 2026  
**Scope:** Six Wave 1 paperbacks only — A01, A04, A05, B10, B12, and B18.  
**Status:** Candidate domain configuration and six draft narration files are prepared. **No QR code may be printed or uploaded until ownership/name clearance, live deployment, audio review, route tests, and physical-proof scans pass.**

## Product rule

Each eligible paperback may include one optional, short audio pause on its copyright / note-before-you-begin page. The experience is a complement to the printed reflection; it is not a treatment, guided medical instruction, therapy, financial advice, or a substitute for professional care.

The QR must resolve to a brand-owned redirect host, not a raw website-builder URL or a consumer shortener printed as the permanent address. A redirect service may be used operationally, but the public printed address remains under the buyer-controlled domain.

## Canonical route map

| SKU | Product | Printed endpoint after domain registration | Landing-page path | Audio asset | On-page label |
|---|---|---|---|---|---|
| A01 | *Dose & Breathe* | `go.stillworkstudio.com/arrive` | `/listen/arrive/` | `A01-arrive.mp3` | A quiet optional pause |
| A04 | *Softer Words* | `go.stillworkstudio.com/soften` | `/listen/soften/` | `A04-soften.mp3` | A quiet optional pause |
| A05 | *Night Harbor* | `go.stillworkstudio.com/harbor` | `/listen/harbor/` | `A05-harbor.mp3` | A quiet optional pause |
| B10 | *Rest & Regulate* | `go.stillworkstudio.com/settle` | `/listen/settle/` | `B10-settle.mp3` | A quiet optional pause |
| B12 | *Back to Enough* | `go.stillworkstudio.com/enough` | `/listen/enough/` | `B12-enough.mp3` | A quiet optional pause |
| B18 | *Enough Money, Enough Calm* | `go.stillworkstudio.com/clarity` | `/listen/clarity/` | `B18-clarity.mp3` | A quiet optional pause |

`stillworkstudio.com` is a **candidate configuration only** in `brand_config.json`; ownership and name clearance have not been independently verified. Do not stamp/print a code until those conditions are documented. Never substitute a temporary test host, Bitly, Rebrandly, Squarespace, Carrd, Linktree, or a local URL in a print file.

## Ownership and redirect design

1. Register the exact domain in the business owner’s account, with renewal, registrar login, DNS, and recovery email documented outside this repository.
2. Use `go.<domain>` for the short printed redirect and `www.<domain>/listen/<route>/` (or another first-party origin) for the destination.
3. Put the redirect map in a buyer-controlled configuration. `qr-routing/worker.js` is a Cloudflare Worker reference implementation; it may be adapted to another managed redirect service only if the public short host remains buyer controlled.
4. Host the six mobile-first landing pages and their audio at the first-party origin. The supplied generator creates plain static pages with no tracker, lead form, or third-party embed by default.
5. Preserve every route indefinitely. If a host, analytics system, or audio provider changes, update the redirect target—not the printed QR image.

## Non-negotiable completion checklist

- [ ] `stillworkstudio.com` is confirmed registered and controlled by the business owner (or `brand_config.json` is changed to the cleared replacement before QR generation).
- [ ] Trademark/name reviewer clears the working imprint and relevant product/series names.
- [ ] A healthcare/claims reviewer clears A01 audio and any other claims-sensitive script; all six scripts have editorial sign-off.
- [ ] The six draft MP3s in `qr-routing/site/audio/` have passed editorial/claims review in `QR_AUDIO_REVIEW.md`, are marked final, and play on mobile with the screen locked/unlocked as intended.
- [ ] Each HTTPS `go.<domain>/<route>` redirects to its expected first-party landing page without an account login, age gate, forced download, tracker, or broken certificate.
- [ ] `python configure_wave1_qr.py --domain <domain> --apply --verify-live` completes successfully after a clean `python build_catalog.py`.
- [ ] QR is at least 1.1 in. square, black on white, surrounded by clear space, and its printed short address appears below it for accessibility.
- [ ] For **each** Wave 1 proof: scan the actual printed page under warm indoor light using an older phone and a current phone; confirm correct route, audio, title, and no unsafe claim.
- [ ] The printed QR is checked again after any KDP trim, page-count, interior, domain, or landing-page change.
- [ ] Proof passes all other KDP and Wave 1 gates before ads are enabled.

## Build order

```bash
# 1. Apply the working imprint and rebuild the base candidate package.
python build_catalog.py

# 2. After the domain is genuinely registered, build deployable pages and QR assets.
python configure_wave1_qr.py --domain example.com --prepare

# 3. Add the reviewed final MP3s in qr-routing/site/audio/, deploy the static site + redirect,
#    then verify and stamp QR artwork into the six Wave 1 interiors.
python configure_wave1_qr.py --domain example.com --apply --verify-live

# 4. Re-run every gate. The QR script is not publication authorization.
python validate_catalog.py
python audit_metadata_claims.py
```

The final stamp operation regenerates only Wave 1 interior PDFs and their actual-page listing samples. It deliberately leaves Wave 2 and Vault paperbacks untouched.
