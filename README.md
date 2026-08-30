# Journals

Product catalogs live on **separate branches**. Do not merge them.

| Branch | Imprint | What |
|---|---|---|
| [`ADHD-Journals`](https://github.com/ifelaniya-byte/Journals/tree/ADHD-Journals) | Quiet Mind Press | 18 journals + coloring · **frozen** `3feca69` |
| [`Range-Band`](https://github.com/ifelaniya-byte/Journals/tree/Range-Band) | Range Band Press | 36 trackers · **frozen** `8562469` |
| [`main`](https://github.com/ifelaniya-byte/Journals/tree/main) | — | Pointer only `8cc3ab5` |
| [`Agent-Seller-Pipeline`](https://github.com/ifelaniya-byte/Journals/tree/Agent-Seller-Pipeline) | — | Pipeline **collaboration surface** (not a trust boundary) |

## New chat

Paste [`NEW_CHAT.md`](NEW_CHAT.md) into the next Arena session, then run [`restore_workspace.sh`](restore_workspace.sh).

That script clones catalogs under `/tmp` and keeps this pipeline tree separate so interiors cannot contaminate the station.

## Seller pipeline (this branch)

- `omega-station/` — reflective station (other agent)
- `omega-seller-station/` — Omega/Shadow station (this agent)
- `SELL_HUB.md` — 54-SKU sell sequence (not a book file)
- Mock actor by default. No model weights. No auto-publish.

True isolation is still a **private** repo. See `GOVERNANCE.md` and `omega-seller-station/REMOTE.md`.
