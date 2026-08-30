# Separate GitHub repository

This pipeline must **not** live on `ifelaniya-byte/Journals`.

| Ref | SHA (2026-08-29) | Role |
|---|---|---|
| `ADHD-Journals` | `3feca69` | Quiet Mind Press books |
| `Range-Band` | `8562469` | Range Band Press books |
| `main` | `8cc3ab5` | pointer only |
| `Agent-Seller-Pipeline` | **same as `main`** | not isolation — unprotected public branch |

The Journals deploy key (`github_journals_deploy`) authenticates **only** to `ifelaniya-byte/Journals`. It cannot create a new GitHub repository.

## Owner steps (authenticated account)

1. On GitHub: **New repository** → `ifelaniya-byte/omega-seller-station` → **private** → empty (no README).
2. Add a deploy key or use your account SSH key (not the Journals-only key, unless you add that public key to the new repo too).
3. From this directory:

```bash
git remote add origin git@github.com:ifelaniya-byte/omega-seller-station.git
git push -u origin main
```

Do not force-push Journals. Do not merge this history into `ADHD-Journals` or `Range-Band`.
