# Omega Seller Station

Reflective autonomous **engineering + selling** pipeline.

This is **not** superintelligence. It is a control substrate:

| Piece | Job |
|---|---|
| **Omega** | think (retrieve → math → research → brainstorm → plan → act → critique → revise) |
| **Shadow** | remember / seal / detect corruption / reseal with a reason |
| **Stationary** | inspect and judge — **never secretly fix** |
| **Evolved actor** | the only writer (LLM slot; mock by default) |
| **Engineers** | execute; helpers **propose**, they do not overwrite |
| **Verifiers A/B** | hostile — assume the engineer is wrong |
| **Overseers A/B** | should this be accepted at all? |
| **Evidence ledger** | every claim is auditable |
| **Final gate** | no auto-publish, no KDP upload, no force-push |

Do **not** run this inside the catalog git tree. Air-gap: clone catalogs under `/tmp`, keep this station beside them.

## One-file bootstrap

From the parent of this directory:

```bash
python build_seller_station.py --target ./seller-station --force
```

## Run (mock, no API key)

```bash
cd seller-station
python -m pytest -q
python -m omega init
python -m omega missions missions.example.json
python -m omega run
python -m omega status
python -m omega gate
```

## Live model

```text
OMEGA_PROVIDER=openai-compatible
OMEGA_MODEL=<model>
OMEGA_API_BASE=<endpoint>
OPENAI_API_KEY=<secret>
```

## Hostile policy (this catalog)

Fails verification if copy contains Ozempic / Wegovy / Mounjaro / 75 Hard / cure / diagnose, if **$14.99** is pasted onto KDP/Amazon, if Quiet Mind and Range Band series are mixed, or if the requested action is `kdp_upload` / `amazon_publish` / `force_push`.

Drafts land only in `generated/`. Overseers default to a **human gate**.

## State

```text
.omega/state.sqlite3
.omega/evidence.jsonl
.omega/shadow.json
.omega/repository-map.json
```
