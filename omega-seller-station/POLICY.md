# Binding policy — candidate-only

This station **drafts**. It does not sell.

A named human is required before any of:

- publish, price, spend, list an item for sale
- KDP / B&N / Lulu / Ingram upload
- Amazon, TikTok, Meta, Pinterest, Etsy, Gumroad, Payhip posting
- email, customer contact, credential use
- git force-push, merge of catalog branches, Compare & pull request
- enabling KDP Expanded Distribution

## Always fail (verifier)

- Manufacturer brands: Ozempic, Wegovy, Mounjaro, Saxenda, Zepbound, Rybelsus
- “75 Hard”, cure / diagnose / “treats nausea”
- B&N **$14.99** pasted onto KDP/Amazon copy
- Mixing Quiet Mind Press and Range Band Press on one series page
- Actions: `kdp_upload`, `amazon_publish`, `force_push`, `merge_imprints`, `merge_branches`

## Writes

Actor may write only under `generated/`. Stationary writes nothing. Scanners are read-only.

## Models

No weights in this repository. The actor is an HTTP client. Default provider is **mock**. Live models require `allow_network: true` and still cannot pass the human gate.

## Catalogs

Books live in `ifelaniya-byte/Journals` on `ADHD-Journals` and `Range-Band`. This pipeline must not copy interiors, wraps, or listing kits into itself.
