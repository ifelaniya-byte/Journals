# Governance: the seller channel and its two stations

## Status

- **omega-station/** (this branch): full reflective pipeline v2.3.0 -
  dual scans, jailed LLM actor (any OpenAI-compatible endpoint),
  Stationary judge, dual verifiers, dual overseers, hash-chained
  evidence, git final gate (omega/* branch + PR artifact, never
  auto-merge), credential-scrubbed command sandbox, and untrusted
  proposal-JSON intake implementing the sibling sandbox's
  collaboration protocol. 32/32 tests green.
- **omega-seller-station-sandbox** (other agent's workspace, local
  commit `15ed523`, not pushed): offline candidate-only station
  (POLICY.md / ARCHITECTURE.md / COLLABORATION_PROTOCOL.md). Its
  protocol now interoperates with this station:
  `python3 -m omega_station proposal <file.json>`.

## Shared principles (both stations)

- Candidate-only. The only success state is `PASS_CANDIDATE`;
  publishing, pricing, posting, uploading, deploying, emailing, and
  spending remain named-human gates.
- No credentials in git. No model weights in git - a thin HTTPS
  client calls an external endpoint (hosted API or self-hosted
  Ollama behind a tunnel).
- Hash-chained evidence, verifiable after the fact.
- Air gap from catalog branches: `ADHD-Journals` and `Range-Band`
  stay pristine; data crosses as small exports (prices / banned
  lists).

## The boundary question (honest)

This branch is the **collaboration surface, not a trust boundary**.
It is a public, unprotected branch inside the books repository:
anything here is public and shares the repository's access control.
That is acceptable for code and already-public catalog data (prices
of record), and NOT acceptable for anything sensitive. True
separation is a separate **private** repository.

## Owner checklist (authenticated account, manual)

1. Create an empty **private** repository (e.g.
   `omega-seller-station`) from the venture-controlled account.
2. Notify either agent; the station history (v1 through v2.3.0) is
   held locally and can be pushed as the private repo's `main` in
   one command. No re-import needed.
3. Branch-protect `Agent-Seller-Pipeline` (or reduce it to a pointer
   README) once the private repo exists; protect the catalog
   branches too.
4. Preserve dated screenshots of the fork/network state and record
   the containment decision, per the sandbox station's note.
