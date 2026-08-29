# B&N Press kits - the $14.99 minimum-price edition (18 books)

**LIST 11** (≥120pp). **HOLD 7** thin (firststroke, garden, cozy, botanical, celestial, tidal, soft).

This folder is a SEPARATE edition for the only platform whose minimum
list price ($14.99 print, April 2026) is above our $9.99 catalog price.
Everything else in the repo stays $9.99. Interiors are unchanged.

Per-book kit: bn_front.jpg, bn_back.jpg (both 300 DPI, bleed included),
metadata-bn.txt (paste-ready, $14.99).

| Book | Pages | Trim | Paper | Spine color | Panel px |
|---|---|---|---|---|---|
| architect | 140 | 8.5x11.0 | white | #363C5E | 2588x3375 |
| dump | 200 | 5.5x8.5 | cream | #524438 | 1688x2625 |
| firststroke | 100 | 8.5x11.0 | white | #AC5834 | 2588x3375 |
| fractal | 140 | 8.5x11.0 | white | #161626 | 2588x3375 |
| garden | 100 | 8.5x11.0 | white | #2E663A | 2588x3375 |
| mosaic | 120 | 8.5x11.0 | white | #30486C | 2588x3375 |
| night | 120 | 5.0x8.0 | cream | #1C2030 | 1538x2475 |
| parallel | 160 | 7.0x10.0 | cream | #3E344E | 2138x3075 |
| woodland | 120 | 8.5x11.0 | white | #2A5234 | 2588x3375 |
| botanical | 104 | 8.5x11.0 | white | #1E4E3A | 2588x3375 |
| celestial | 104 | 8.5x11.0 | white | #181A34 | 2588x3375 |
| cozy | 104 | 8.5x11.0 | white | #7C4C38 | 2588x3375 |
| dopamine | 150 | 6.0x9.0 | cream | #9E4A3A | 1838x2775 |
| middle | 160 | 6.0x9.0 | white | #7E405E | 1838x2775 |
| settle | 172 | 6.0x9.0 | cream | #964E36 | 1838x2775 |
| slow | 144 | 6.0x9.0 | cream | #805232 | 1838x2775 |
| soft | 96 | 6.0x9.0 | cream | #546C4A | 1838x2775 |
| tidal | 104 | 8.5x11.0 | white | #104256 | 2588x3375 |

Upload steps: press.barnesandnoble.com -> Create -> Paperback ->
enter metadata from metadata-bn.txt -> upload interior PDF from release3/4 ->
choose separate front/back cover upload -> bn_front.jpg + bn_back.jpg ->
spine color from the table -> price $14.99 -> publish.

Regenerate any time: python3 make_bn_kits.py
