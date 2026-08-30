# Architecture

```
GITHUB CATALOG REPOS (untouched)
        │  read-only facts, never cloned into this tree
        ▼
  OMEGA RECON MAP
        │
   SCAN A     SCAN B     (independent; no shared conclusions)
        │         │
        └── consensus ── Shadow seal
                │
         Stationary (judge, no writes)
                │
         Omega loop: retrieve → math → research → brainstorm
                     → plan → act → critique → revise
                │
         Evolved actor (LLM *client* or mock)
                │
         Engineers (propose; helpers do not overwrite)
                │
      VERIFIER A     VERIFIER B     (hostile)
                │
      OVERSEER A     OVERSEER B     (should this exist at all?)
                │
         PASS_CANDIDATE / HOLD / REWORK / ESCALATE
                │
         named human gate  →  sell
```

## Implemented

- Dual Shadow scans + consensus + SHA-256 seals + reseal-with-reason
- Stationary directives; Stationary cannot write the judged tree
- Reflective loop with sealed stage outputs
- Mock actor + OpenAI-compatible client (OpenRouter / Groq / Together / Ollama)
- Fail-closed network: live models refused unless `allow_network`
- Hostile policy verifier (blacklist, price drift, imprint mix, blocked actions)
- Dual overseers; `auto_merge` stays false
- SQLite state + JSONL evidence ledger
- Writes confined to `generated/`

## Deliberately excluded

- Model weights, Git LFS, local 1B+ checkpoints
- Autonomous publish / price / spend / marketplace APIs
- PRs into `ADHD-Journals` or `Range-Band`
- Force-push, Expanded Distribution, mixing imprints
- Running inside the catalog git working tree

## Brain vs nervous system

This repo is the nervous system (~hundreds of KB of Python). Inference is HTTPS to an interchangeable endpoint. Swap:

| Provider | `OMEGA_PROVIDER` | `OMEGA_API_BASE` |
|---|---|---|
| mock (default) | `mock` | — |
| OpenRouter | `openai-compatible` | `https://openrouter.ai/api/v1` |
| Groq | `openai-compatible` | `https://api.groq.com/openai/v1` |
| Ollama on loopback | `ollama` | `http://127.0.0.1:11434/v1` |

No pipeline code changes when the brain moves.
