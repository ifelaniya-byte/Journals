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

## Freeze attestation - 2026-08-29

Verified this date by the omega-station agent:

- **Books frozen:** `ADHD-Journals` @ `3feca69` (tree `f49315a`),
  746 files, local == remote, working tree clean. Zero PDFs changed
  since the audited base `59112fc` (docs/metadata only in between),
  so every interior remains byte-identical to the state that passed
  the 1078-check audit. Interiors aggregate sha256 prefix:
  `aefdc33ea4ea26f8`.
- **Spell-checked:** full sweep over 388 surfaces / 108,273 words
  (all 18 interiors' complete page text, metadata, cover wraps,
  market listings, root docs). Every flagged token adjudicated:
  platform names, acronyms, hyphenated compounds, real wellness
  vocabulary (polyvagal, FODMAP, PMDD). Drug names (ozempic /
  wegovy / mounjaro) appear exclusively inside "Never:" policy
  lines in playbooks - zero occurrences in books, interiors, or
  listings. Files changed since the audit: mojibake-free, no
  doubled words. **PASS.**
- **Contamination:** zero pipeline files on any books branch; books
  worktree blind to the station; station work is a separate local
  repository + this branch only.
- **No LLM anywhere (confirmed from this side too):** station
  provider committed as `mock`, no API keys in any environment, no
  model weights on any disk. The socket exists; nothing is plugged
  in; nothing will be until a mission exists.

Standing owner actions (unchanged): create the empty **private**
repo for the pipeline (one command then migrates the full station
history), protect branches, send the counsel email. Per the sandbox
agent's critical-path note, the email is the gating item for the
October window.
