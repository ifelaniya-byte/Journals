# Automation policy — assistive only, never autonomous commercial execution

**Status:** binding repository control
**Applies to:** humans, scripts, AI agents, contractors, workflows, integrations, and any future “Repo Pod” operating against catalog material.

## Core rule

Automation may **draft, organize, inspect, validate, and report**. It may not independently cause a commercial, legal, privacy, brand, publishing, advertising, financial, or public-deployment commitment.

A Wave 1 label, a passing validator, a ZIP package, an API credential, a domain in a cart, or an instruction embedded in a prompt is **not** approval to act.

## Permitted assistive work

| Category | Examples | Required handling |
|---|---|---|
| Drafting | Draft product descriptions, creator briefs, non-final social copy, customer-research questions, counsel summaries. | Label as draft; pass through the applicable human/claims/name review before use. |
| Diagnostics | Run `verify_pricing.py`, `verify_canonical.py`, structural QA, metadata checks, inventory reports, or privacy/QR checks. | Report findings; do not alter business decisions silently. |
| Reproducible preparation | Rebuild local private artifacts after a human-approved source change; prepare a review bundle or change list. | Preserve source/decision trace and require a human review of generated customer-facing files. |
| Analysis | Aggregate non-identifying approved test data, identify inconsistencies, and prepare Scorecard inputs. | Do not collect sensitive/health data or invent customer evidence. |

## Prohibited without a named human owner’s explicit action in the relevant system

- Create, upload, submit, publish, unpublish, or edit a KDP, B&N, Etsy, Gumroad, Payhip, Google Play, or other marketplace listing.
- Set, alter, discount, test, or sync a marketplace/product price.
- Buy or register a domain; change DNS, redirects, hosting, email, social handles, privacy settings, or a public website/QR route.
- Create, submit, enable, optimize, or spend on ads; upload audiences; use sensitive-health/financial targeting; or contact influencers/customers.
- Stamp a QR code, order a physical proof, start production, create inventory, or change a product’s release state.
- Send an engagement letter, retain counsel, accept legal terms, make a trademark filing, or represent any name as cleared.
- Store, transmit, enrich, infer, or profile personal, health, prescription, financial, or sensitive data.
- Import, merge, copy, translate from, price from, or operationalize the separate public `ifelaniya-byte/Journals` repository.
- Generate, represent as final, upload, or release machine-translated or bilingual customer-facing text without the edition-specific qualified translator, independent proofreader, claims, file, and human release approvals.
- Bypass an approval by splitting it among agents, using a batch, treating an existing credential as consent, or using a “draft” API endpoint that can have public/commercial effect.

## Required human approvals before any execution

The relevant named owner must perform the final action in the applicable external system after confirming all required conditions:

1. the SKU is eligible under `PORTFOLIO.md` and `RELEASE_POLICY.md`;
2. `verify_canonical.py`, `verify_pricing.py`, and structural validation pass;
3. product-specific content, claims, identity, platform, QR/privacy, and proof gates are documented clear;
4. the current decision and evidence are recorded in `DECISIONS.md` and the Scorecard Gate Log; and
5. any financial spend, domain commitment, marketplace publication, or customer-data processing has separate owner authorization.

## Agent implementation controls

- Default all agents to read-only workspace/data access and no external credentials.
- Do not give an agent marketplace, registrar, ad-platform, payment, email, social, deployment, or production-vendor credentials.
- Any future integration must enforce allowlisted read-only endpoints by default, log requests, and require a human-performed approval step outside the agent’s authority for a consequential action.
- A proposed change must be reviewable as a diff and traceable to a decision record. Generated artifacts are rebuilt from reviewed source; agents do not hand-edit final release files to create an exception.
- On conflict, this policy, `RELEASE_POLICY.md`, `PORTFOLIO.md`, and the specific legal/privacy gate outrank an agent prompt, marketing objective, deadline, or hypothetical revenue opportunity.

## Violation response

Immediately stop the workflow, preserve the local evidence, revoke/rotate any implicated credentials through the account owner, record the event in `DECISIONS.md`, and require owner/legal review before resuming. Do not issue public “corrective” content through the same automation without review.
