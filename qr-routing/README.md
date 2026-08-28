# First-party QR routing deployment

This directory is a deployable-reference architecture, not a live service and not an instruction to print QR codes yet.

## Intended production topology

- **Printed URL:** `https://go.<owned-domain>/<route>`
- **Redirect:** buyer-controlled DNS + Worker/configuration in this directory
- **Destination:** `https://www.<owned-domain>/listen/<route>/`
- **Audio:** static MP3 and transcript hosted at the destination origin

Never print a raw Carrd, Shopify, Squarespace, Bitly, Rebrandly, Linktree, temporary tunnel, platform preview, or local address. Those can be operational destinations during setup, but the permanent print address must be buyer controlled.

## Files

- `worker.js` — small Cloudflare Worker reference map for the six permanent routes.
- `routes.json` — generated only after an exact domain is supplied to `configure_wave1_qr.py`.
- `site/` — generated mobile-first static landing pages and final reviewed MP3 destination folder.

## Deployment outline

1. Register and document the domain in the business owner’s account.
2. Create DNS for `go.<domain>` and point it to the chosen redirect host; deploy `worker.js` or equivalent buyer-controlled routing configuration.
3. Run `python configure_wave1_qr.py --domain <domain> --prepare`. Put reviewed final MP3s into `site/audio/`.
4. Publish `site/` at `www.<domain>` (or substitute the configured first-party origin); set `LANDING_ORIGIN` to that origin.
5. Test every HTTPS redirect on mobile and desktop. Then run `--apply --verify-live` to stamp the Wave 1 interiors.
6. Test actual printed proofs; only a passing proof can clear the QR gate.

The redirect needs a maintained ownership and renewal record. A dead QR is a product defect.
