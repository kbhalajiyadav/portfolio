# Research Notes lifecycle and private incubation

This document defines **where** Research Notes are allowed to exist during capture, drafting, testing, review, publication, correction, retirement, and archival. Its primary purpose is to prevent a false assumption that `draft: true`, an unlisted URL, or a private account automatically makes research private.

## 1. Core boundary

The `kbhalajiyadav/portfolio` repository is public. Therefore:

> **Anything committed or pushed to this repository must already be safe for public disclosure, even when Hugo marks it `draft: true`.**

`draft: true` means only **not rendered on the public website**. It does not mean confidential, private, embargoed, or undiscoverable. Public Git history, branches, pull requests, forks, caches, APIs, mirrors, and local clones may preserve committed material.

Unpublished research, collaborator-confidential material, sponsor-restricted information, uncleared patent-sensitive details, embargoed manuscript material, regulated/restricted data, or other non-public work must remain outside this public repository.

## 2. Storage authority before tooling

The private workspace is a research-data/storage decision before it is a writing-tool decision.

VCU currently directs university personnel to classify data and use its Data Management System (DMS) to determine which storage, transmission, and processing services are allowable for the relevant information type:

- <https://infosec.ts.vcu.edu/how-to/how-do-i-classify-and-store-my-data/>
- <https://infosec.ts.vcu.edu/resources/data/dms/>
- <https://infosec.ts.vcu.edu/resources/data/>

VCU describes Category II data as including proprietary information, properly de-identified research information, intellectual property, internal communications, and other sensitive university information. Therefore a **private GitHub repository is not assumed to be an approved home for unpublished university research merely because its visibility is private**.

Use a local or institutionally approved storage/service appropriate to the actual data classification. If the content type, sponsor, protocol, IP status, or applicable storage rule is uncertain, resolve that before choosing cloud synchronization or remote hosting.

## 3. Lifecycle states

The system uses six practical states.

### A. Embryo — private capture

Purpose: raw thinking, questions, fragments, literature notes, chat-derived prompts, rough diagrams, experimental interpretation, and early writing.

Storage: a local Obsidian vault or another institutionally permitted private/approved storage location.

Allowed content: unpublished or incomplete material only to the extent that the chosen storage and tools are authorized for that material.

Never deploy or synchronize this layer to the public portfolio repository.

### B. Incubation — private drafting and reasoning

Purpose: structure an idea into a possible public note; develop argument, backlinks, figures, headings, citations, and information architecture.

Recommended authoring environment: Obsidian plus a **local-only Quartz 5 preview** when its graph, backlinks, search, transclusions, or Markdown rendering improve thinking.

Quartz is a rendering and knowledge-navigation tool, not a confidentiality control. Quartz 5 supports filter plugins that decide which pages are emitted, including a built-in draft-removal pattern, but filtering generated output does not make source Markdown private when the underlying storage/repository is public.

Authoritative Quartz references:

- <https://quartz.jzhao.xyz/>
- <https://quartz.jzhao.xyz/advanced/making-plugins>

Default rule: the private Quartz environment is **not deployed publicly**. Remote/private deployment is considered only if the storage, authentication, hosting, institutional rules, and data classification have been reviewed and are appropriate.

### C. Clearance — private promotion review

Purpose: decide whether a candidate is safe to leave the private research workspace.

Clearance includes, as applicable:

- disclosure basis;
- collaborator/PI review;
- ownership and sponsor obligations;
- journal/preprint/conference/embargo status;
- IP/patent review;
- human/animal/regulated research;
- export-control and dual-use considerations;
- conflicts of interest;
- copyright/figure rights;
- contributor credit;
- funding acknowledgement;
- privacy/consent;
- citation/source-status review;
- AI/external-tool data-governance constraints.

A calendar date alone never auto-clears an embargo. Human review is required before promotion.

### D. Private release candidate — local web QA

Purpose: test a cleared or nearly cleared candidate with the actual Hugo templates, figures, metadata, links, responsive behavior, accessibility, and local audit scripts **without pushing it to GitHub**.

Recommended implementation: a local clone/worktree of the portfolio, or another local testing copy, that is not pushed until the candidate is repository-safe.

This stage allows the full editorial/web experience to be tested while the candidate remains non-public. Run the same local checks documented in the repository README.

If the candidate still contains material that is not authorized for the local testing environment, keep it in the private research workspace instead. Local testing does not waive data-classification requirements.

### E. Public-source staging — public Git source, website still optional

Purpose: perform final PR/CI review on material that is already safe to disclose publicly.

Location: `content/notes/` in this public repository.

Required state:

- `governance.repository_safe: true`;
- all public-repository boundary checks pass;
- `draft: true` may remain temporarily if website/editorial QA is incomplete or if public source disclosure is intentional before website release.

At this stage the source is **already public** even though the site page may not be rendered.

If the goal is “nothing is discoverable before launch,” do not use public-source staging for the note body. Complete testing in the private release-candidate stage and treat the first public push/PR as the disclosure event.

### F. Published — canonical public note

Purpose: publish the reviewed note at `bhalaji.com/notes/...`.

Requirements:

- all governance and evidence checks pass;
- web/accessibility/performance checks pass;
- author release decision is explicit;
- `draft: false`;
- canonical live page is verified after deployment.

Only after canonical publication may POSSE/syndication occur.

## 4. Private archive versus public history

There are two different archives.

### Private archive

Unpublished ideas that are paused, abandoned, superseded before disclosure, or retained for future research stay in the approved private workspace. They may be archived or deleted there according to applicable research-data, retention, sponsor, protocol, and institutional rules.

They should never be copied into the public repository merely for version control.

### Public history

Once a note has been published or its source pushed publicly, assume the disclosure cannot be reversed. Deleting a Git commit, branch, pull request, or webpage does not reliably restore secrecy.

Previously public material that becomes incorrect or unsuitable should normally use a correction, withdrawal, retirement notice, or redirect rather than pretending the disclosure never occurred.

## 5. Correction and withdrawal states

Use these public lifecycle states:

- `evolving` — valid public note expected to develop;
- `stable` — mature public note with low expected conceptual change;
- `corrected` — substantive public correction exists;
- `retired` — superseded or no longer maintained, with destination/context where appropriate;
- `withdrawn` — content should no longer be relied upon; retain a minimal notice explaining the status without unnecessarily repeating material that should not continue to circulate.

Never use withdrawal as a substitute for pre-publication disclosure review.

## 6. One-way promotion rule

The safe flow is:

`private embryo -> private incubation -> private clearance -> private release candidate -> public-source staging -> published -> maintained/corrected/retired`

Movement into public Git is a one-way disclosure boundary.

Do not implement automatic two-way synchronization between the private vault and `content/notes/`. Automatic sync creates an unnecessary failure mode in which a private file, attachment, rename, transclusion, or metadata change can leak into a public build or Git commit.

Promotion should be deliberate and one-directional.

## 7. Quartz role

Quartz 5 may be used for the private authoring experience because it supports Markdown/Obsidian workflows, backlinks, search, graphs, transclusions, and publication filters. The production portfolio remains Hugo and the existing bhalaji.com visual system.

Recommended separation:

```text
private/approved Obsidian vault + local Quartz preview
                       |
                       | deliberate, cleared promotion
                       v
private local Hugo release candidate
                       |
                       | first intentional public disclosure
                       v
public Hugo portfolio repository -> bhalaji.com
```

Do not couple the production site's deployment to the private Quartz vault.

## 8. Local workspace safety

Prefer keeping the real private vault as a **sibling directory outside the public repository** so an accidental recursive Git operation cannot stage it.

For example:

```text
Research/
├── research-vault/        # private, appropriately classified/approved storage
└── portfolio/             # public Git repository
```

The public repository also ignores convenience directory names such as `.research-incubator/`, `embryo/`, and `private-research/`. `.gitignore` is only an accident barrier; it is not a security boundary.

Tracked local Git hooks in `.githooks/` run `scripts/check_notes_governance.py` before commit and before push once the repository is configured to use them:

```bash
git config core.hooksPath .githooks
```

The hooks are a local safety net. They can be bypassed and therefore do not replace judgment, storage controls, or remote CI.

## 9. Attachments and figures

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

## 10. AI and external-tool boundary

The private workspace may contain information that must not be supplied to external AI, cloud, or publishing services. Tool use is governed by the data classification and applicable institutional, sponsor, collaboration, protocol, IP, and confidentiality requirements.

Do not treat a tool's private-account setting, private repository, unlisted URL, or `draft` flag as authorization to upload restricted research material.

## 11. Minimal operational rule

This architecture intentionally avoids a complicated CMS or multi-environment deployment system.

The minimum reliable workflow is:

1. classify/store appropriately;
2. write privately;
3. preview privately with Obsidian/Quartz when useful;
4. clear disclosure privately;
5. test the release candidate locally with Hugo and local audits;
6. move/push only repository-safe material into public Git;
7. publish on the website only after final gates pass;
8. syndicate only after canonical publication;
9. maintain a visible correction/retirement history after publication.

The safety comes from clear storage boundaries, deliberate one-way promotion, local pre-disclosure checks, and remote fail-closed validation — not from adding a complex publishing stack.