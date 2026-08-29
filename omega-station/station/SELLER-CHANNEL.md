# Seller channel: how this station serves the catalogs

## The contract (air gap)

Catalog branches (`ADHD-Journals` = Quiet Mind Press 18 books,
`Range-Band` = Range Band Press 36 trackers) are pristine product.
The station NEVER runs inside them and NEVER pushes to them.
Catalog data arrives here as small exported files:

```text
seller/prices-<imprint>.json    title -> price of record
banned-phrases.txt              phrases that must never ship
```

Flow: actor drafts copy/assets -> hostile policy verifier (banned
phrases with negation guard, price drift vs the export, required
disclaimers) -> verified assets land in a review queue with the
hash-chained evidence trail -> a named human publishes. Publishing,
pricing, and listing are human gates, always - the automation
prepares, people decide.

## Collaboration on this branch

- `omega-station/` is the station (builder + generated runtime +
  tests + demo). Interface guaranteed stable: the policy CLI
  `python3 -m omega_station policy <file> --title <t> --prices
  <json> --banned <txt> --require-disclaimer`.
- Sibling directories are yours; add queue/UI/exports freely.
- Do not merge catalog branches into this one.

## Imprint-specific risk notes

- Quiet Mind Press (journals/coloring): keep the medical-advice
  disclaimer discipline; prices of record = paperback column.
- Range Band Press (GLP-1 / wellness trackers): this is the lethal
  category for claims. Default banned list already blocks
  ozempic/wegovy/mounjaro, cure/guarantee, clinically proven,
  fda approved, doctor recommended. Extend per listing; when in
  doubt, escalate to the human reviewer.

## Models

No model weights live in this repository, ever. The station calls
an OpenAI-compatible endpoint (hosted API or a self-hosted Ollama
box behind a tunnel); see the endpoint table in
`station/README.md`. Cost stays fractions of a cent per call and is
capped by the station's enforced model-call budget.
