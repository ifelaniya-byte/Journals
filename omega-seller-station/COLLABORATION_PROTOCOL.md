# Collaboration protocol (other AI)

You do not get write access to the catalog branches. You submit an **untrusted local proposal**.

## Proposal file

`proposals/<id>.json`

```json
{
  "mission_id": "MKT-QM-12-002",
  "title": "Draft three Pinterest lines",
  "action": "draft_copy",
  "output_path": "generated/example.json",
  "requirements": ["tracking/management only", "KDP $9.99 if priced"],
  "files": ["generated/example.json"],
  "mock_body": "optional; live models ignore this"
}
```

Forbidden keys: `action` in `kdp_upload`, `amazon_publish`, `force_push`, `merge_imprints`.

## How it is processed

1. Proposal is copied into a disposable candidate directory.
2. Shadow scans A/B run on the candidate, not on Journals.
3. Actor may write only `generated/**`.
4. Verifiers A/B attack claims vs disk vs policy.
5. Overseers A/B decide HOLD vs PASS_CANDIDATE.
6. Catalog trees are never modified.

## Do not

- Open a Compare & pull request against `ADHD-Journals`, `Range-Band`, or `main`
- Commit interiors, wraps, listing images, or `SELL_HUB.md` here
- Put API keys or model weights in the proposal
- Ask the station to publish
