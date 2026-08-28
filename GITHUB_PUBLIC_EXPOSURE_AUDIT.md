# Public GitHub exposure audit — urgent owner action

**Observed:** August 28, 2026
**Scope:** publicly readable information at `https://github.com/ifelaniya-byte/Journals` and GitHub’s public API. This local repository has no configured remote and cannot administer that GitHub repository.

## Finding

`ifelaniya-byte/Journals` is a **public**, non-archived GitHub repository created on August 28, 2026. It is distinct from this local controlled catalog: its commit history, branch names, product names, and remotes do not overlap with the local `ritual-library-kdp-catalog` history.

Public API/repository pages showed:

| Exposure item | Public observation | Risk |
|---|---|---|
| Visibility | Public; forkable; not archived; no tags. | Anyone can view, clone, or preserve the content while it remains public. |
| Branches | `main`, `ADHD-Journals`, `Range-Band`; all unprotected. | Multiple unrelated product catalogs are exposed outside this repository’s controls. |
| `main` | A pointer README identifies the two product branches. | Makes the sensitive branches easy to find. |
| `Range-Band` | Public README describes 36 undated GLP-1/wellness trackers, every KDP title at `$9.99`; a later commit describes `$14.99` B&N print and `$9.99` PDFs. | Directly conflicts with the controlled catalog’s six-scout, claims-review, premium-price, and no-autonomous-release rules. |
| `ADHD-Journals` | Public branch describes 18 prompt journals/coloring books under a separate imprint, with `$9.99` price enforcement. | Unreviewed claims/positioning and unwanted product association may be publicly visible. |
| Recent activity | Commits were public and actively updating at the time of inspection. | Do not assume a static historical ZIP; exposure may still be changing. |

## Required containment (account owner only)

1. **Immediately make `ifelaniya-byte/Journals` private** in GitHub repository Settings → General → Danger Zone → Change visibility, or delete it if it has no required evidence value. Do not first “clean it up” with public commits; those commits add more public history.
2. On the same account, review and remove/lock down all three branches: `main`, `Range-Band`, and `ADHD-Journals`. For an unwanted project, delete the repository rather than merely deleting a branch.
3. If retention is needed, make the repository private first, export an evidence archive, then create a new private, access-controlled repository only after counsel and product review.
4. Disable forking on any retained private repository; review repository collaborators, deploy keys, personal access tokens, GitHub Apps, Actions secrets, webhooks, Pages, releases/packages, wiki, issues, discussions, and any external deployment links.
5. Search connected KDP, B&N, Gumroad, Payhip, Google Play, social, ad, domain, and email accounts for the exposed titles/imprints. Remove drafts/listings/campaigns or preserve evidence for counsel; do not publish corrective content that repeats sensitive claims.
6. Ask counsel whether the public exposure affects the search/common-law, claim-review, takedown, or brand-rollout path. Preserve screenshots/commit URLs privately if needed.

## What this local repository can and cannot do

- **Can:** document the exposure, retain a governance record, block any attempt to import its pricing/claims/release strategy, and keep the current catalog’s validators/release gates strict.
- **Cannot:** change visibility, delete branches, invalidate clones/forks, rotate GitHub credentials, delete external listings, or determine account ownership without authenticated access and owner direction.

## Explicit separation rule

Do not merge, copy, re-price from, or automate publishing from `ifelaniya-byte/Journals`. Its `$9.99` materials are not source data for this catalog. The controlled portfolio remains an 18-concept private option library with exactly six potential Wave 1 KDP scouts, all subject to product-specific counsel, price, technical, QR/privacy, and proof gates.
