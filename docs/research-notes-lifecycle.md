# Research Notes lifecycle and private incubation

This document defines **where** Research Notes are allowed to exist during drafting, review, publication, correction, retirement, and archival. Its primary purpose is to prevent a false assumption that `draft: true` makes research private.

## 1. Core boundary

The `kbhalajiyadav/portfolio` repository is public. Therefore:

> **Anything committed to this repository must already be safe for public disclosure, even when Hugo marks it `draft: true`.**

`draft: true` means only **not rendered on the public website**. It does not mean confidential, private, embargoed, or undiscoverable. Public Git history, forks, caches, APIs, mirrors, and local clones may preserve committed material.

Unpublished research, collaborator-confidential material, sponsor-restricted information, uncleared patent-sensitive details, embargoed manuscript material, regulated/restricted data, or other non-public work must remain outside this repository.

## 2. Lifecycle states

The system uses five practical states.

### A. Embryo — private capture

Purpose: raw thinking, questions, fragments, literature notes, chat-derived prompts, rough diagrams, experimental interpretation, and early writing.

Storage: a local Obsidian vault or another institutionally permitted private/approved storage location.

Allowed content: unpublished or incomplete material only to the extent that the chosen storage and tools are authorized for that material.

Never deploy or sync this layer to the public portfolio repository.

### B. Incubation — private drafting and testing

Purpose: structure an idea into a possible public note; test backlinks, figures, headings, citations, and information architecture.

Recommended authoring environment: Obsidian plus a **local-only Quartz 5 preview** when its graph, backlinks, search, or Markdown rendering improve thinking.

Quartz is a rendering and knowledge-navigation tool, not a confidentiality control. Quartz 5 supports filter plugins that decide which pages are emitted, including a built-in draft-removal pattern, but filtering generated output does not make source Markdown private if the source repository/storage is public.

Authoritative Quartz references:

- <https://quartz.jzhao.xyz/>
- <https://quartz.jzhao.xyz/advanced/making-plugins>

Default rule: the private Quartz environment is **not deployed publicly**. Remote/private deployment is considered only if the storage, authentication, hosting, institutional rules, and data classification have been reviewed and are appropriate.

### C. Clearance — private promotion review

Purpose: decide whether a candidate is safe to leave the private workspace.

The candidate must pass the publication-governance review before copying any prose, figures, attachments, or source material into the public repository.

Clearance includes, as applicable:

- disclosure basis;
- collaborator/PI review;
- ownership and sponsor obligations;
- journal/preprint/embargo status;
- IP/patent review;
- human/animal/regulated research;
- export-control and dual-use considerations;
- conflicts of interest;
- copyright/figure rights;
- contributor credit;
- funding acknowledgement;
- privacy/consent;
- citation/source-status review;
- AI-input/data-governance constraints.

A calendar date alone never auto-clears an embargo. Human review is required before promotion.

### D. Public-source staging — public repository, not website

Purpose: perform editorial, design, CI, accessibility, structured-data, responsive, Lighthouse, and rendering review on material that is already safe to disclose.

Location: `content/notes/` in this public repository.

Required state:

- `governance.repository_safe: true`;
- all public-repository boundary checks pass;
- `draft: true` may remain while website/editorial QA is incomplete.

At this stage the source is public even though the site page is not rendered.

This is the only meaning of `draft: true` in the portfolio repository.

### E. Published — canonical public note

Purpose: publish the reviewed note at `bhalaji.com/notes/...`.

Requirements:

- all governance and evidence checks pass;
- web/accessibility/performance checks pass;
- author release decision is explicit;
- `draft: false`;
- canonical live page is verified after deployment.

Only after canonical publication may POSSE/syndication occur.

## 3. Private archive versus public history

There are two different archives.

### Private archive

Unpublished ideas that are paused, abandoned, superseded before disclosure, or retained for future research stay in the private workspace. They may be archived or deleted there according to the applicable research-data and institutional rules.

They should never be copied into the public repository merely for version control.

### Public history

Once a note has been published or its source committed publicly, assume the disclosure cannot be reversed. Deleting a Git commit or webpage does not reliably restore secrecy.

Previously public material that becomes incorrect or unsuitable should normally use a correction, withdrawal, retirement notice, or redirect rather than pretending the disclosure never occurred.

## 4. Correction and withdrawal states

Use these public lifecycle states:

- `evolving` — valid public note expected to develop;
- `stable` — mature public note with low expected conceptual change;
- `corrected` — substantive public correction exists;
- `retired` — superseded or no longer maintained, with destination/context where appropriate;
- `withdrawn` — content should no longer be relied upon; retain a minimal notice explaining the status without repeating material that should not continue to circulate.

Never use withdrawal as a substitute for pre-publication disclosure review.

## 5. One-way promotion rule

The safe flow is:

`private embryo -> private incubation -> private clearance -> public-source staging -> published -> maintained/corrected/retired`

Movement into the public repository is a one-way disclosure boundary.

Do not implement automatic two-way synchronization between the private vault and `content/notes/`. Automatic sync creates an unnecessary failure mode in which a private file, attachment, rename, or transclusion can leak into a public build or Git commit.

Promotion should be deliberate and one-directional.

## 6. Quartz role

Quartz 5 may be used for the private authoring experience because it supports Markdown/Obsidian workflows, backlinks, search, graphs, transclusions, and filters. The production portfolio remains Hugo and the existing bhalaji.com visual system.

Recommended separation:

`private Obsidian vault + local Quartz preview`

`        | explicit cleared export/copy`

`public Hugo portfolio repository`

Do not couple the production site's deployment to the private Quartz vault.

## 7. Local workspace safety

The public repository reserves local-only directory names such as `.research-incubator/`, `embryo/`, and `private-research/` in `.gitignore`. These are convenience barriers, not confidentiality controls.

Prefer keeping the real private vault as a **sibling directory outside the public repository** so an accidental recursive Git operation cannot stage it.

For example:

```text
Research/
├── research-vault/        # private, institutionally appropriate storage
└── portfolio/             # public Git repository
```

This physical separation is safer than relying only on `.gitignore`.

## 8. Attachments and figures

A candidate is not repository-safe merely because its Markdown prose is safe. Promotion review includes every associated:

- image;
- PDF;
- CSV/data file;
- diagram source;
- screenshot;
- photograph;
- code snippet;
- embedded/transcluded note;
- metadata/EXIF payload.

Photographs and exported assets should be checked for visible confidential material and unnecessary metadata before entering the public repository.

## 9. AI and external-tool boundary

The private workspace may contain information that must not be supplied to external AI, cloud, or publishing services. Tool use is governed by the data classification and applicable institutional, sponsor, collaboration, protocol, IP, and confidentiality requirements.

Do not treat a tool's private-account setting, unlisted URL, or `draft` flag as authorization to upload restricted research material.

## 10. Minimal operational rule

This architecture intentionally avoids a complicated CMS or multi-environment deployment system.

The minimum reliable workflow is:

1. write privately;
2. preview privately if useful;
3. clear disclosure privately;
4. copy only the cleared candidate into the public repository;
5. keep it `draft: true` while web QA occurs;
6. publish by changing to `draft: false` only after final gates pass;
7. maintain a visible correction/retirement history after publication.

The safety comes from a clear storage boundary and fail-closed promotion checks, not from adding more publishing infrastructure.