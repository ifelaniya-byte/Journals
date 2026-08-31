# Quiet Mind Press — Push Status

Date: 2026-08-31
Target repo: `ifelaniya-byte/Journals` (private, confirmed via GitHub API)
Session branch: `arena/01a058a3-journals`

## Summary

This file records the truthful state of the "push the entire Quiet Mind Press workspace"
request. It also documents what could NOT be shipped from this session.

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
