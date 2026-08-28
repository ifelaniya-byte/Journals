# Public GitHub exposure audit — urgent owner action

**Observed:** August 28, 2026
**Scope:** publicly readable information at `https://github.com/ifelaniya-byte/Journals` and GitHub’s public API. This local repository has no configured remote and cannot administer that GitHub repository.

## Finding

`ifelaniya-byte/Journals` is a **public**, non-archived GitHub repository created on August 28, 2026. It is distinct from this local controlled catalog: its commit history, branch names, product names, and remotes do not overlap with the local `ritual-library-kdp-catalog` history.

Public API/repository pages showed:

| Exposure item | Public observation | Risk |
|---|---|---|
| Visibility | Public; forkable; not archived; no tags. | Anyone can view, clone, or preserve the content while it remains public. |
| Branches | `main`, `ADHD-Journals`, `Range-Band`, `Market-Files`; all publicly reported as unprotected. | Multiple unrelated product/market-asset workstreams are exposed outside this repository’s controls. |
| `main` | A pointer README identifies the two product branches but does not document `Market-Files`. | Makes some sensitive branches easy to find while potentially obscuring other public assets. |
| `Range-Band` | Public README describes 36 undated GLP-1/wellness trackers, every KDP title at `$9.99`; public market material describes B&N print and digital price paths. | Directly conflicts with the controlled catalog’s six-scout, claims-review, premium-price, and no-autonomous-release rules. |
| `ADHD-Journals` | Public branch describes 18 prompt journals/coloring books under a separate imprint, a retailer playbook, and translated storefront-copy paths while keeping interiors English. | Unreviewed claims/positioning, multilingual-copy, pricing, and unwanted product association may be publicly visible. |
| `Market-Files` | Public README describes B&N cover panels, 17 printable PDFs, and two lead magnets. | Potential commercial assets must not be assumed owned, copied, or deployed from this catalog. |
| Recent activity | Commits were public and actively updating at the time of inspection. | Do not assume a static historical ZIP; exposure may still be changing. |

## Public evidence snapshot and ownership question

At the latest unauthenticated, read-only public-API check on August 28, 2026, GitHub reported the repository as public, non-archived, forkable, with `forks_count: 0` and `network_count: 0`; its four public branches were `main`, `ADHD-Journals`, `Range-Band`, and `Market-Files`. This is a dated public-observation record, not proof that no one has cloned or copied content elsewhere. The account/controller relationship cannot be determined from public data.

**Before any merge, separation, or commercial use decision, the founder must identify which statement is true and record the answer in `DECISIONS.md`:**

| If the account is… | Required decision |
|---|---|
| Controlled by this venture / a collaborator | Either bring it under these controls (private repository, no public releases, per-SKU gates, no copied pricing/copy/trade dress) or formally firewall it as a separate business with different identity, copy, assets, audiences, and storefronts. Do not leave a same-owner undercutting GLP-1/wellness catalog in ambiguous parallel operation. |
| Controlled by the founder personally but outside this project | Make it private or delete it, then decide whether any reviewed non-sensitive learning may be migrated through a documented, fresh review. No wholesale import or history merge. |
| Controlled by an unrelated third party | Preserve the dated public evidence, do not contact through an automated channel, and obtain counsel’s direction on confidential-information, claim, trademark, and takedown implications. |
| Unknown | Treat it as external/untrusted until a named controller confirms otherwise; do not merge, copy, or share credentials/material. |

For a human screenshot, the account owner should capture the repository landing page, branches page, fork/network count, each exposed README, and recent commit history **before** changing visibility. Save the images privately with date/time and URLs; do not post them as a public issue or “cleanup” commit.

## Required evidence-first containment (account owner only)

1. **Before changing public visibility or branches, privately preserve evidence:** capture dated screenshots of the repository landing page, every branches page, fork/network state, each exposed README, recent commit history, releases/packages, Pages, wiki, issues, and actions artifacts. Save exact URLs and time zone. Do not create a public “cleanup” issue or commit.
2. In the authenticated account, check the live fork/network graph and determine who controls `ifelaniya-byte` (founder, collaborator, unrelated third party, or unknown). Record the relationship and the chosen merge-under-governance vs firewall/separation path in `DECISIONS.md`.
3. **After that evidence/relationship step,** make `ifelaniya-byte/Journals` private or delete it if it has no required evidence value, as the authenticated owner and counsel direct. Do not assume zero public API forks means no historical clone/copy exists.
4. Review and remove/lock down all four branches: `main`, `Range-Band`, `ADHD-Journals`, and `Market-Files`. For an unwanted project, delete the repository rather than merely deleting a branch.
5. If retention is needed, make the repository private first, export an evidence archive, then create a new private, access-controlled repository only after counsel and product review.
6. Disable forking on any retained private repository; review repository collaborators, deploy keys, personal access tokens, GitHub Apps, Actions secrets, webhooks, Pages, releases/packages, wiki, issues, discussions, and any external deployment links.
7. Search connected KDP, B&N, Gumroad, Payhip, Google Play, social, ad, domain, and email accounts for the exposed titles/imprints. Remove drafts/listings/campaigns or preserve evidence for counsel; do not publish corrective content that repeats sensitive claims.
8. Ask counsel whether the public exposure affects the search/common-law, claim-review, takedown, or brand-rollout path. Preserve screenshots/commit URLs privately if needed.

## What this local repository can and cannot do

- **Can:** document the exposure, retain a governance record, block any attempt to import its pricing/claims/release strategy, and keep the current catalog’s validators/release gates strict.
- **Cannot:** change visibility, delete branches, invalidate clones/forks, rotate GitHub credentials, delete external listings, or determine account ownership without authenticated access and owner direction.

## Explicit separation rule

Do not merge, copy, re-price from, or automate publishing from `ifelaniya-byte/Journals`. Its `$9.99` materials are not source data for this catalog. The controlled portfolio remains an 18-concept private option library with exactly six potential Wave 1 KDP scouts, all subject to product-specific counsel, price, technical, QR/privacy, and proof gates.
