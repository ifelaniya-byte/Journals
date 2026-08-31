# Quiet Mind Press — Push Status

Date: 2026-08-31
Target repo: `ifelaniya-byte/Journals` (private, confirmed via GitHub API)
Session branch: `arena/01a058a3-journals`

## Summary

This file records the truthful state of the "push the entire Quiet Mind Press workspace"
request. It also documents what could NOT be shipped from this session.

## Product counts (as of 2026-08-31)

| Category | Count | Status |
|---|---|---|
| QMP frozen catalog products on private repo (`ADHD-Journals`) | 18 | Pushed / verified on remote |
| Wave A (`qmp-wave-a/ready`) | 8 | NOT pushed — source not in this session |
| Wave B (`qmp-wave-b/ready`) | 10 | NOT pushed — source not in this session |
| Next-36 (`qmp-next-36/ready`) | 36 | NOT pushed — source not in this session |
| Deep-36 (`qmp-deep-36/ready`) | 36 | NOT pushed — source not in this session |
| Existing digital editions (exact frozen copies, `qmp-all-36/existing-digital`) | 17 | NOT pushed — source not in this session |
| All-36 manifest + validation (`qmp-all-36`) | n/a | NOT pushed — source not in this session |
| Seller pipeline / handoff (`quiet-mind-restore/pipeline`, `SELL_HUB.md`, `GOVERNANCE.md`) | n/a | Existing `Agent-Seller-Pipeline` branch is on remote; QMP workspace copy not pushed |

Reconciliation (QMP candidate universe): 18 existing + 8 (Wave A) + 10 (Wave B) + 36 (Next-36)
+ 36 (Deep-36) = 108 product candidates; plus 17 existing digital editions (separate digital
products that are exact copies of frozen interiors, subtract the one print-only title).

- **Pushed QMP products: 18** (the frozen catalog on `ADHD-Journals`).
- **Pushable from this session's live filesystem: 0 additional QMP products** — the
  `qmp-*` / `quiet-mind-restore` trees are not present on the live disk in this session.
- **Unfinished / not on remote: 90 QMP product candidates** (8 + 10 + 36 + 36), plus the 17
  existing digital editions, the all-36 manifest, and the QMP-side pipeline/handoff files.
- **Excluded by policy:** Range-Band 36-book line (`Range-Band` branch) and the Range-Band
  Deep-36 line (`range-band/DEEP-NEED-36` on `arena/01a054fa-journals`) — these are the
  read-only Range Band imprint and are intentionally kept separate from QMP.

## Shipped / verified on the private repo

- `arena/01a058a3-journals` @ `3feca690a77a636ada6ca840e73c5c02a83f1c0f`
  - Frozen Quiet Mind Press catalog checkout (`ADHD-Journals` source, 18 frozen products).
  - Verified on the remote via GitHub API. No product uploads, publication, or sales-channel
    changes were made. All candidates remain `HOLD_HUMAN_REVIEW`.
- Existing remote branches (present before this session, no changes made):
  - `ADHD-Journals`
  - `Agent-Seller-Pipeline`
  - `Market-Files`
  - `Range-Band` (read-only, kept isolated)
  - `ritual-library-catalog`
  - `ritual-library-production-batch`

## NOT shipped — source missing from session filesystem

The following products/pipelines were NOT present on the live filesystem in this session and
therefore could not be pushed. They are listed here exactly so a future session with the
workspace restored can push them without re-deriving the scope.

- `qmp-wave-a` — Wave A, 8 products (`home-reset`, `meals-without-the-maze`,
  `time-in-view`, `study-small-steps`, `habit-map`, `gentle-routine`,
  `botanical-mysteries`, `big-bold-mandalas`) — print + digital candidates.
- `qmp-wave-b` — Wave B, 10 products (`start-small`, `mood-weather`, `after-the-sting`,
  `family-flow`, `stained-glass-nature`, `cottagecore-creatures`, `gothic-botanica`,
  `birds-in-bloom`, `mushroom-forest`, `enchanted-libraries`) — print + digital candidates.
- `qmp-all-36` — `CATALOG_36.csv`, `existing-digital/` (17 exact frozen digital copies +
  Gumroad ZIPs).
- `qmp-next-36` — Next-36, 36 candidates (18 planners/128p + 18 coloring/96p).
- `qmp-deep-36` — Deep-36, 36 planner/log candidates (128p each).
- `quiet-mind-restore/` — pipeline + handoff (`pipeline/`, `NEW_CHAT_IMPROVED.md`,
  `restore_workspace_safe.sh`, `SELL_HUB.md`, `GOVERNANCE.md`, validation reports).

## Verification performed

- Scanned `/home/user`, `/tmp/arena-workspace`, and common mount/upload paths.
- Searched the filesystem for `qmp-*` trees and key build/validation files.
- `git fsck --full --no-reflogs --unreachable` returned 0 dangling objects; no local Git
  history contains the QMP trees.
- Searched every remote branch tree; only Range-Band's `DEEP-NEED-36` exists and is
  intentionally excluded (Range-Band is read-only and isolated from QMP).

## Do not do

- Do not upload, publish, price, advertise, send email, or create accounts for any QMP
  candidate. All are `HOLD_HUMAN_REVIEW`.
- Do not regenerate frozen interiors. Do not mix QMP with Range-Band.
- Do not delete local `ready/` binaries until the corresponding trees are confirmed on the
  remote.
