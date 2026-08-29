# Omega Station

A reflective autonomous engineering pipeline, generated from one file.

```text
build_omega_station.py  ->  python3 build_omega_station.py --target .
```

## Architecture

```text
Repository
    |
    +-- Shadow Scan A (filesystem walk)   independent
    +-- Shadow Scan B (git index + grep)  independent
    |
Consensus map (confirmed / single-source / disputed - never silently resolved)
    |
Omega mission generator (findings -> verifiable engineering missions)
    |
per mission:
    seals BEFORE
    -> Omega plan
    -> Actor (LLM or mock) in a budgeted, scope-jailed tool loop
    -> seals AFTER
    -> Stationary judge (observe + directives only; it cannot fix)
    -> Verifier A: spec (machine-checkable commands)
    -> Verifier B: hostile (cheats, secrets, regressions, ledger chain)
    -> Overseer A: value (churn/scope)   Overseer B: risk (budgets, human gate)
    -> ACCEPT -> reseal | REWORK -> directives feed the next attempt
               | ESCALATE (incl. missions that require a human)
```

## Use

```bash
python3 build_omega_station.py --target . --force
python3 -m unittest discover -s tests -q      # generated test suite
python3 -m omega_station recon                # dual scans + consensus
python3 -m omega_station missions             # mission list
python3 -m omega_station run                  # full loop (mock provider)
python3 -m omega_station status
python3 -m omega_station ledger               # verify evidence chain
python3 -m omega_station integrity            # seals vs filesystem
python3 -m omega_station policy copy.txt --title "The Settle Journal" \
    --banned banned-phrases.txt --prices prices.example.json \
    --require-disclaimer
```

## Real LLM in the actor slot (the model never lives here)

The station is a ~2KB thin HTTPS client, never model weights. A 1B
or frontier model serves any number of stations from one external
endpoint; weights never belong in git (GitHub stores, it does not
run). Swap endpoints without touching pipeline code:

| Setup | OMEGA_API_BASE | OMEGA_MODEL (example) |
|---|---|---|
| Deterministic mock (default, no key) | - | - |
| OpenRouter | https://openrouter.ai/api/v1 | qwen/qwen-2.5-7b-instruct |
| Groq | https://api.groq.com/openai/v1 | llama-3.1-8b-instant |
| Ollama box via tunnel | https://<tunnel>.trycloudflare.com/v1 | qwen2.5:1.5b |
| Any OpenAI-compatible | your endpoint | your model |

```bash
export OMEGA_PROVIDER=openai-compatible
export OMEGA_MODEL=<model>
export OMEGA_API_BASE=<endpoint>
export OMEGA_API_KEY=<secret>   # env only - never in git; scrubbed
python3 -m omega_station run    # from actor-spawned commands too
```

Transient network faults retry twice with backoff, then fail CLOSED:
the mission escalates instead of proceeding on a guess. Usage tokens
are recorded per call against the station-wide call budget.

The actor speaks a strict one-action-per-turn JSON tool protocol
(read / list / write / edit / run / finish). Writes and edits are
denied outside mission scope. Network commands are denied unless
explicitly allowed. Every step lands in the evidence ledger.

## Honest capability table

| Capability | State |
|---|---|
| Shadow seals / corruption detection / reseal | implemented + tested |
| Hash-chained evidence ledger | implemented + tested (tamper detected) |
| Dual independent scans + consensus | implemented (filesystem + git) + tested |
| Stationary judge separation | implemented (no write tools by construction) |
| Jailed actor tool loop (LLM slot) | implemented; mock is deterministic |
| Dual verifiers (spec + hostile) | implemented + tested |
| Dual overseers (value + risk) | implemented + tested |
| Rework with directive feedback | implemented (v1 lost failures; v2 feeds them back) |
| Budget enforcement (calls / steps / runtime) | implemented + enforced |
| Marketing policy verifier (banned/price/disclaimer) | implemented + tested |
| Untrusted proposal-JSON intake (collaboration protocol) | implemented + tested: candidate-only copies, intake gates, scope/hash verify, PASS_CANDIDATE requires named human review |
| Persistent seals (cross-session integrity) | implemented + tested |
| Resume after restart (state/ledger/seals) | implemented + tested |
| Git branch isolation + per-mission commits | implemented + tested |
| PR artifact + optional push/PR creation | implemented + tested (local); remote needs OMEGA_PUSH / OMEGA_GH_TOKEN |
| HTTP actor path (OpenAI-compatible endpoint) | implemented + tested end-to-end vs local mock server (reactive brain, usage recorded, garbage output escalates) |
| Credential hygiene in command sandbox | implemented + tested (API keys/tokens scrubbed from actor processes) |
| Resource limits (CPU / mem / file / nproc) + TMPDIR isolation | implemented + tested (Linux rlimits) |
| Real frontier model as actor | protocol + HTTP path proven; swap in any endpoint + key |
| Container/production sandboxing | not implemented (network denial is heuristic) |
| Automatic merge/deploy | deliberately never implemented: merge is a human decision |

This is an engineering-integrity substrate, not superintelligence.
The intelligence is whatever you put in the actor slot; the value is
that nothing it does is trusted until it survives verification.

## Collaboration protocol (untrusted proposals)

Another agent (or the sibling sandbox station) submits a proposal
JSON: `allowed_paths` (exact files it may write), `files` (contents),
optional `run_tests` (python/unittest allowlist only). The station
verifies it candidate-only:

```bash
python3 -m omega_station proposal proposal.json \
    --banned banned-phrases.txt --prices prices.example.json
```

Intake gates reject publish/price/upload/network actions before
anything is copied. Writes land in a fresh disposable candidate
copy; hash-diff must equal the declared scope exactly; optional
allowlisted tests run jailed; policy audit covers every written
file. The only success state is PASS_CANDIDATE - named human review
required. The source tree is never modified.

## Final gate (git flow)

Accepted missions are committed to an `omega/station-*` branch (one
commit per verified mission) while the base branch is never touched.
`.omega/PR.md` carries the mission table + ledger status. Set
`OMEGA_PUSH=1` to push the branch, `OMEGA_GH_TOKEN` to open the PR.
The station never merges - reviewing and merging is a human decision.

## Command sandbox (honest scope)

Actor-spawned commands run with: workspace cwd jail, dangerous-command
blocklist, heuristic network denial, a scrubbed environment (nothing
matching KEY/TOKEN/SECRET/PASS/CREDENTIAL/AUTH, plus SSH/git/loader
injection vars, reaches the child; the station's own OMEGA_API_KEY
cannot be printed back out), a private TMPDIR, and Linux rlimits
(CPU / address space / file size / process count). This is meaningful
hygiene, NOT a container: a determined actor process can still read
files inside the workspace. For untrusted models, run the station in
a container or VM - that boundary stays out of scope by design.

## Air-gap rule

Run the station in its own working copy or sandbox, never inside a
pristine production catalog. Missions that represent trust decisions
(committing someone's work, publishing, deploying) are generated as
requires_human and escalate rather than act.

## The mock provider is honest

It drives the real tool loop with scripted actions per mission type
so the whole control plane (jails, seals, verifiers, overseers,
ledger, budgets) is exercised without model credits. It is labeled
mock in every ledger record.
