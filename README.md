# Bhalaji Yadav Kantepalle — Research Portfolio

Official source for [bhalaji.com](https://bhalaji.com), a Hugo-based academic
portfolio and generated curriculum vitae.

## Repository structure

- `data/portfolio.yaml` — profile, chronology, and public records
- `data/cv.yaml` — structured source for the two-page CV
- `data/site_controls.yaml` — presentation limits and feature controls
- `content/` — research and portfolio pages
- `layouts/` — Hugo templates
- `assets/` and `static/` — styles, scripts, and published assets
- `scripts/` — deterministic build and validation utilities

Content classification decisions are recorded in
`docs/content-taxonomy.md`. Sitewide hierarchy, scientific-visual integrity,
responsive composition, evidence-link behavior, spacing, social-preview
behavior, and release lessons are recorded in `docs/design-governance.md`.

Research publishing uses five separate controls:

- `docs/research-notes-governance.md` — **can** the material be publicly disclosed?
- `docs/research-publishing-visibility-strategy.md` — **should** it be published, and how should it compound into credible discovery?
- `docs/research-notes-lifecycle.md` — **where** drafting, private incubation, local release testing, public-source staging, publication, correction, retirement, and archival are allowed to occur.
- `docs/research-notes-design-standard.md` — **how** a public note should read, look, perform, remain accessible, and handle scientific figures/citations/revisions.
- `docs/research-notes-tooling-evaluation.md` — **which tools** own each part of the workflow and which alternatives are intentionally not adopted.

These documents are intended to carry forward into future changes rather than
be rediscovered case by case.

## Research Notes disclosure boundary

This repository is public. Therefore `draft: true` is **not a privacy control**:
it prevents Hugo from rendering a note on the website, but the Markdown source
would still be public through GitHub if committed or pushed.

Unpublished research, confidential/collaborator material, embargoed content,
uncleared patent-sensitive information, restricted data, and other non-public
work stay outside this repository in an institutionally appropriate private
workspace. Storage/service choices for VCU research should follow the applicable
data classification and VCU Data Management System guidance rather than assume
that a private third-party repository is automatically approved.

The recommended lifecycle is:

`private embryo -> private incubation -> private clearance -> private local release candidate -> repository-safe public source -> website publication -> maintenance/correction`

Obsidian and a local-only Quartz 5 preview may support the private incubation
stage. Quartz is an authoring/navigation layer, not a confidentiality boundary;
the private vault is not coupled to the public Hugo deployment.

Quarto is reserved as an optional scientific-authoring/compiler layer for notes
that genuinely need bibliography automation, cross-references, equations,
numbered figures/tables, or reproducible computational output. Hugo remains the
only production renderer and owner of the public visual system. The controlled
Quarto + curated Zotero/Better-BibTeX pilot for Note 001 is tracked in issue #79.

Required tooling remains free/open-source or part of the existing repository and
hosting stack. Optional integrations must have a genuine free tier or a
verifiable academic/student-access route; paid-only tools are not core
dependencies.

## Local pre-disclosure guard

The repository includes executable `pre-commit` and `pre-push` hooks that run
the Research Notes governance checker before a candidate leaves the local
machine. Enable the tracked hooks once per clone:

```bash
npm run setup:hooks
```

or equivalently:

```bash
git config core.hooksPath .githooks
```

These hooks are an accident barrier, not an authorization system; they can be
bypassed and do not replace correct private storage or human disclosure review.
Remote GitHub Actions repeats the guard as a second line of defense.

## Research Notes publication gate

`archetypes/notes.md` is deliberately fail-closed. A generated note cannot be
committed safely until `governance.repository_safe: true` is defensible and the
public-repository boundary reviews are resolved.

`scripts/check_notes_governance.py` enforces the boundary for both Hugo drafts
and published notes. It rejects public-repository candidates containing
unpublished/collaborator/confidential material, active embargoes, unresolved IP
or venue restrictions, incomplete ownership/contributor/funding/privacy/tool or
copyright review, unresolved ethics/export/dual-use checks, or invalid COI
metadata. Website publication adds source-status and explicit author-release
requirements.

The dedicated GitHub Actions workflow runs on every pull request and main-branch
change, plus a monthly schedule and manual dispatch.

A passing automated check is necessary but not sufficient: scientific,
disclosure, ownership/collaboration, IP, venue, ethics/COI, privacy, copyright,
and other judgments still require appropriate human review under the governing
institutional, sponsor, journal, protocol, and collaboration requirements.

## Dependency and merge safety

Dependabot monitors GitHub Actions and npm dependencies. GitHub Dependency Graph
is enabled, and pull requests run the official dependency-review action pinned
to an immutable commit SHA. Dependency review is configured to fail on newly
introduced vulnerabilities at moderate severity or higher.

Repository administration should require the `build`, `governance`, and—after
successful validation on PR #77—`dependency-review` checks in the `main`
ruleset. Issue #78 tracks these ruleset changes so the administrative control
cannot be silently forgotten.

## Build and validation

The validated local sequence is:

```bash
python3 -m pip install PyYAML==6.0.3 websocket-client==1.9.0
bash scripts/build_browser_icons.sh
python3 scripts/build_social_cards.py
python3 scripts/build_cv.py --no-compile
python3 scripts/audit_source.py
python3 scripts/audit_styles.py
python3 scripts/audit_templates.py
python3 scripts/check_design_governance.py
python3 scripts/check_notes_governance.py
python3 scripts/check_workflows.py
node --check assets/js/site.js
node --check assets/js/evidence-target.js
hugo --gc --minify --printPathWarnings --baseURL https://bhalaji.com/
python3 scripts/check_site.py public
python3 scripts/check_social_previews.py public
python3 scripts/check_external_links.py public --site-origin https://bhalaji.com/
```

GitHub Actions also runs accessibility, responsive-layout, contextual-navigation,
deep-link and dismissal-state, spacing, component-integrity, laptop-frame, and
mobile/desktop Lighthouse checks before deployment. Research Notes have an
additional repository/publication-governance workflow, and pull requests receive
dependency review. CV compilation is handled by the dedicated XeLaTeX workflow.

## Rights

Copyright © 2026 Bhalaji Yadav Kantepalle. All rights reserved. The repository
is publicly viewable but is not released under an open-source license. Files
that state a separate license remain governed by that license. See `LICENSE`
for the applicable terms.