# Quiet Mind Press — Push Runbook

Target: **private** `ifelaniya-byte/Journals`
Related: `QMP_PUSH_HELPER.sh`, `QMP_PUSH_STATUS.md`

## Status snapshot (2026-08-31)

| Item | Quantity | State |
|---|---|---|
| Frozen QMP catalog products | 18 | On remote (`ADHD-Journals`) |
| Wave A candidates | 8 | Awaiting source restore |
| Wave B candidates | 10 | Awaiting source restore |
| Next-36 candidates | 36 | Awaiting source restore |
| Deep-36 candidates | 36 | Awaiting source restore |
| Existing digital editions | 17 | Awaiting source restore |
| QMP pipeline/handoff | n/a | Awaiting source restore |

## Why it is blocked this session

The product trees (`qmp-wave-a`, `qmp-wave-b`, `qmp-all-36`, `qmp-next-36`,
`qmp-deep-36`, `quiet-mind-restore`) are **not present on the live filesystem**. They are
also absent from every git branch and every commit in the private repo history. Therefore
they cannot be pushed truthfully from this session.

## Steps to finish the full push

1. Restore the real workspace trees into `/home/user` so these exist:
   - `/home/user/qmp-wave-a`
   - `/home/user/qmp-wave-b`
   - `/home/user/qmp-all-36`
   - `/home/user/qmp-next-36`
   - `/home/user/qmp-deep-36`
   - `/home/user/quiet-mind-restore`

2. Confirm the trees are real files (not empty placeholders):
   ```bash
   ls -la /home/user/qmp-* /home/user/quiet-mind-restore
   du -sh /home/user/qmp-* /home/user/quiet-mind-restore | sort
   ```

3. Run the safe report:
   ```bash
   bash /home/user/Journals/QMP_PUSH_HELPER.sh
   ```

4. If the report shows every tree present, stage and push to the private repo:
   ```bash
   bash /home/user/Journals/QMP_PUSH_HELPER.sh --push --branch qmp-workspace
   ```

5. Verify on the remote before believing it:
   ```bash
   git ls-remote origin qmp-workspace
   curl -s https://api.github.com/repos/ifelaniya-byte/Journals/branches/qmp-workspace
   ```

6. Only after verifying the remote, may local `ready/` binaries be considered safe to free up.

## Hard rules enforced by the helper

- Never regenerates frozen interiors or product content.
- Excludes the Range-Band catalog tree (`quiet-mind-restore/catalogs/range-band`) and
  never copies Range-Band books into a QMP branch.
- Does not embed or request credentials; it uses the existing git origin credential.
- Refuses to run if origin is not `ifelaniya-byte/Journals`.
- Refuses to stage/push until all required trees are present.

## What is already pushed (do not redo)

- `ADHD-Journals` — frozen 18-product catalog.
- `Agent-Seller-Pipeline` — existing pipeline branch.
- `Market-Files`, `Range-Band`, `ritual-library-catalog`,
  `ritual-library-production-batch` — existing branches (Range-Band is read-only/isolated).
- `arena/01a058a3-journals` — session branch carrying `QMP_PUSH_STATUS.md`,
  `QMP_PUSH_HELPER.sh`, and this runbook.
