# New-chat restore — paste this as the first message

You are continuing Quiet Mind Press / Range Band Press work on Arena.ai.

**Do not merge branches. Do not force-push. Do not upload to KDP/B&N. Do not connect a live LLM until listings exist. Do not copy catalog PDFs into the pipeline tree.**

## Restore (run first)

```bash
chmod 600 /home/user/.ssh/github_journals_deploy   # if the key is in this workspace
export GIT_SSH_COMMAND='ssh -i /home/user/.ssh/github_journals_deploy -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new'
bash /home/user/pipeline/restore_workspace.sh
```

If this workspace is empty, clone the pipeline branch first:

```bash
git clone --single-branch --branch Agent-Seller-Pipeline \
  git@github.com:ifelaniya-byte/Journals.git /home/user/pipeline
bash /home/user/pipeline/restore_workspace.sh
```

## Source of truth (verify SHAs)

| What | Git | Branch | Expected tip |
|---|---|---|---|
| Quiet Mind 18 books | `ifelaniya-byte/Journals` | `ADHD-Journals` | `3feca69` |
| Range Band 36 books | same | `Range-Band` | `8562469` |
| Pointer | same | `main` | `8cc3ab5` |
| Pipeline + this handoff | same repo, **wrong building** | `Agent-Seller-Pipeline` | newest on that branch |
| True isolation | **does not exist yet** | private repo `omega-seller-station` | owner must create |

Catalogs are **frozen**: $9.99 KDP × 54 paperbacks, spell-checked, no pipeline files on those branches.

## Layout after restore

```
/tmp/qmp-adhd              ADHD-Journals (books — read/commit only that branch)
/tmp/Journals-remote       Range-Band (books — read/commit only that branch)
/home/user/pipeline        Agent-Seller-Pipeline (code only, no interiors)
/home/user/SELL_HUB.md     54-SKU sell sequence
```

Work books under `/tmp`, never copy `release*/` or `KDP-Complete-Kit/` PDFs into `/home/user/pipeline`.

## Pipeline

Two stations on the pipeline branch (mock actor, HTTPS client, no weights):

- `omega-station/` — other agent’s v2 station
- `omega-seller-station/` — this agent’s Omega/Shadow station (`fb34491` lineage)

Both are candidate-only. Success = `PASS_CANDIDATE` / HOLD. Human gate for publish/price/spend.

## Still required from the owner

1. Create empty **private** GitHub repo `ifelaniya-byte/omega-seller-station` and move pipeline history there. This branch is a collaboration surface, not a trust boundary.
2. Do not plug a live model until there are live listings.
3. Wave 1 KDP (when you actually list): QM Dopamine / 75 Soft / Middle Season / Cozy; RB 01 / 09 / 05 / 30 / 10 / 12. ED off. No ads on RB 14.

Read `SELL_HUB.md`, `GOVERNANCE.md`, `omega-seller-station/POLICY.md`. Then continue the user’s actual request — do not reopen frozen interiors.
