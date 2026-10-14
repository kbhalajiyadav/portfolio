# Research Notes publication governance

This document is the release standard for Research Notes associated with the portfolio. It is deliberately conservative: a personal research website and its public Git repository are public-disclosure channels, not substitutes for laboratory, sponsor, journal, university, ethics, technology-transfer, or legal review.

The default rule is **fail closed**. If disclosure status, ownership, confidentiality, attribution, intellectual-property status, ethics, venue restrictions, privacy, or conflict-of-interest treatment is uncertain, keep the material in the private incubation workspace described in `research-notes-lifecycle.md`.

## 1. Scope, authority, and the public-repository boundary

These rules apply to every Research Note and associated asset.

The `kbhalajiyadav/portfolio` repository is public. Therefore **anything committed here is already publicly disclosed at the source level**, regardless of Hugo's `draft` flag. `draft: true` means only “do not render this page on bhalaji.com yet.” It does not mean private, confidential, embargoed, or undiscoverable.

A note may enter `content/notes/` only after `governance.repository_safe: true` is defensible and all public-repository boundary checks have been resolved.

The standard is grounded in current authoritative guidance, including:

- [VCU Research and Innovation — policies, procedures and compliance notices](https://research.vcu.edu/integrity-and-compliance/compliance/policies-procedures-and-compliance-notices/), covering research integrity/compliance areas including conflicts of interest, intellectual property, export compliance and research security, research data, human/animal research, misconduct, and sponsored-program obligations;
- [VCU conflicts of interest in research](https://research.vcu.edu/integrity-and-compliance/integrity-and-ethics/conflicts-of-interest-in-research/);
- [VCU research ethics consultation](https://research.vcu.edu/integrity-and-compliance/research-ethics-consultation/), including authorship/publication and research-integrity questions;
- [HHS Office of Research Integrity RCR Casebook](https://ori.hhs.gov/rcr-casebook-introduction), addressing authorship/publication, collaboration, data management, conflicts, mentoring, and social responsibility;
- [WIPO patent FAQ](https://www.wipo.int/en/web/patents/faq_patents) and [WIPO patent-protection guidance](https://www.wipo.int/en/web/patents/protection), which caution that public disclosure can affect novelty/patentability;
- [USPTO international patent guidance](https://www.uspto.gov/patents/basics/international-protection/filing-patents-abroad), because patent consequences differ across jurisdictions;
- [ICMJE recommendations on overlapping/public dissemination](https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/overlapping-publications.html), because journal, preprint, conference, and embargo rules can constrain further public dissemination;
- [Crossref Crossmark](https://www.crossref.org/crossmark/), because a citation can be real yet later corrected, updated, or retracted;
- [CRediT contributor roles](https://credit.niso.org/), as a useful standard when substantive contributions need explicit attribution.

When a university policy, sponsor agreement, journal policy, collaboration agreement, protocol, law, regulation, or formal instruction is more restrictive than this repository standard, the more restrictive requirement controls.

## 2. Permitted public-disclosure bases

A note entering the public repository must rest on a defensible public-disclosure basis:

1. `public_literature` — established public sources such as peer-reviewed literature, standards, authoritative technical guidance, or public datasets;
2. `published_own_work` — already-public paper, thesis, dataset, software release, published patent record, or other stable public scholarly record; or
3. `authorized_public_disclosure` — material already made public through an authorized channel, such as a cleared public presentation.

A manuscript being drafted, under review, accepted but embargoed, discussed internally, shown in a closed meeting, stored in a private repository, or contained in a non-public patent application is **not** public merely because later release is expected.

## 3. Absolute public-repository hold conditions

Do **not commit** a note or asset to this repository if it contains or materially reveals:

- unpublished experimental results, trends, images, datasets, formulations, parameters, or mechanistic conclusions;
- unpublished work of a collaborator, laboratory member, student, mentor, or external partner;
- confidential, NDA-bound, sponsor-restricted, export-controlled, security-sensitive, embargoed, or otherwise restricted information;
- enabling details of potentially patentable subject matter that have not been cleared for public disclosure;
- peer-review material, grant-review material, internal research discussions, or non-public sponsor communications;
- identifiable/restricted human-subject information, non-public regulated data, or material inconsistent with an approved protocol or data-use condition;
- third-party figures, tables, photographs, text, or other copyrighted material without an applicable license, permission, or defensible original replacement.

Absence of numbers is not sufficient. A workflow, schematic, choice of variables, sequence of operations, interpretation, or framing can itself reveal unpublished intellectual contribution.

## 4. PI, collaborator, ownership, and contributor rule

If another researcher could reasonably say “this is partly our unpublished work,” hold the material privately until the appropriate author/PI/collaborator review is resolved.

If work was performed using university resources, within a laboratory, under sponsored research, under a collaboration, or in connection with institutional intellectual property, ownership/disclosure obligations must be checked before public-repository entry.

`ownership_review: complete` means the author has checked applicable ownership, collaboration, sponsor, or laboratory obligations; it does not claim sole personal ownership of every underlying asset.

`contributor_review: complete` means substantive intellectual, methodological, software, visualization, supervisory, or writing contributions have been considered for appropriate credit. When useful, CRediT roles can guide attribution. Do not publicly name contributors merely to create an acknowledgement if doing so would disclose sensitive context or if permission is needed.

## 5. Intellectual property

Treat both the public repository and the public website as public disclosure.

If material is potentially patent-sensitive, set `potentially_patent_sensitive: true`. It cannot enter this repository unless `ip_clearance: cleared` and the candidate stays within the cleared public scope.

A filed application does not automatically authorize disclosure of every related implementation detail. A published patent application makes the published contents public, but undisclosed improvements, data, know-how, or later inventions can remain sensitive.

When uncertain, use the relevant institutional technology-transfer/IP channel before repository entry.

## 6. Journal, preprint, conference, and embargo status

A note that overlaps with a manuscript, accepted article, conference disclosure, preprint, or other venue must be checked against the applicable venue/publicity policy.

Use:

- `venue_policy_review: not_applicable` when no relevant venue restriction exists;
- `venue_policy_review: cleared` when the applicable policy has been checked and permits the proposed public disclosure.

`embargo_status` must be `none` before material enters this public repository. An embargo end date does not trigger automatic publication; a human re-review is required after the restriction expires.

## 7. Ethics, regulated research, export control, and dual use

Human participants, animals, regulated data, controlled technology, export restrictions, dual-use concerns, or another formal oversight regime require compatibility with the applicable authorization, protocol, data-use terms, and institutional requirements.

These are separate questions:

- `regulated_research_material` + `ethics_review` address protocol/regulated-research concerns;
- `export_control_review` addresses export/research-security restrictions;
- `dual_use_review` addresses dual-use concerns where applicable.

Ordinary materials-science notes with no such issues use the corresponding `not_applicable` values.

## 8. Privacy and non-research personal information

Research-regulation status does not exhaust privacy risk. Screenshots, photographs, teaching examples, student work, internal messages, sample labels, badges, whiteboards, email excerpts, or collaborator names can expose personal or sensitive information.

`privacy_review: complete` means the note and every associated asset have been reviewed for unnecessary personal information, consent/permission needs, and context-specific privacy obligations.

## 9. Conflicts of interest and funding

Every public-source candidate receives a COI review.

Use:

- `coi_status: none_declared` — no relevant conflict identified for the note;
- `coi_status: disclosed` — a relevant relationship exists and a suitable public statement is provided;
- `coi_status: managed` — a relevant relationship is subject to a formal management arrangement and the public statement is appropriate.

Potentially relevant interests include financial interests, consulting/advisory relationships, employment, sponsorship, licensing interests, inventorship/patent interests, or other relationships a reasonable reader could consider relevant.

`funding_review: complete` means any applicable award terms, acknowledgement language, grant identifiers, sponsor disclaimers, and publication clauses have been considered. Do not publish confidential award documents or management plans as repository evidence.

The repository records only minimal release status; authoritative institutional records remain in their proper systems.

## 10. Citation, source status, and evidentiary calibration

A published note requires independently verified sources and must distinguish:

- established scientific claims — primary literature, standards, or authoritative sources where practicable;
- the author's published results — corresponding paper, thesis, dataset, software release, patent publication, or other public record;
- interpretation — explicitly framed as interpretation and grounded in evidence;
- reflection/methodological preference — clearly framed as perspective rather than universal fact.

Citations must be checked against the underlying source. AI output, search snippets, or secondary summaries are not substitutes for source verification.

`source_status_review: complete` means important sources have also been checked for known corrections, updates, expressions of concern, or retractions where such status information is available. Crossmark and publisher records are useful for DOI-backed literature.

## 11. AI/external-tool input governance

AI or external tools may assist outlining, language editing, adversarial review, or public-source synthesis, but they are not evidentiary authorities.

More importantly, **input governance precedes output governance**. Do not supply non-public research, collaborator-confidential information, sponsor-restricted material, regulated data, unpublished peer/grant review material, or IP-sensitive details to an external AI/cloud service unless that use is permitted by all applicable institutional, sponsor, collaboration, protocol, data-governance, and confidentiality requirements.

`external_tool_review: complete` means the author has considered whether drafting/review tools received material they were permitted to receive. It does not create or imply institutional approval.

Raw AI/chat transcripts are not publication-ready source material.

## 12. Copyright, figures, photographs, and metadata

Every public-source candidate requires `copyright_review: complete`.

Figures are classified as:

- original schematic;
- original data already cleared for public use;
- public/openly licensed data or figure used within its license;
- adapted figure with appropriate rights and attribution;
- reproduced figure with permission;
- clearly labelled illustrative/simulated material;
- photograph with appropriate rights and disclosure clearance.

Illustrative/simulated material must never be presented as observed evidence.

Images and exported assets must also be reviewed for visible confidential information and unnecessary metadata such as location/device information before repository entry.

## 13. Repository-safe metadata versus publication metadata

A note committed to this public repository must already satisfy the **repository-safe gate**:

- `repository_safe: true`;
- valid disclosure basis;
- unpublished/collaborator/confidential flags explicitly false;
- IP review resolved;
- venue policy resolved and no active embargo;
- ethics/export/dual-use questions resolved;
- ownership, contributor, funding, privacy, external-tool, copyright, and COI review resolved.

A note may remain `draft: true` after that while public-site QA continues.

A note with `draft: false` additionally requires:

- non-empty final body/summary;
- verified source list;
- `source_status_review: complete`;
- `author_release_decision: approved`;
- successful web/accessibility/performance/metadata checks.

`author_release_decision` is the author's final publication action. It must never be described as institutional, sponsor, PI, journal, ethics, or legal approval unless such approval actually exists through the appropriate external process.

## 14. Corrections, retirement, and withdrawal

Publication creates an effectively irreversible public record. Deleting a page or Git commit does not reliably restore confidentiality.

After publication:

- minor spelling/layout/link fixes may be corrected without a substantive notice;
- substantive scientific clarification updates `lastmod` and receives a short revision note;
- material factual errors receive a visible correction;
- superseded material may be retired and redirected/contextualized;
- content that should no longer be relied upon receives a withdrawal notice rather than silent deletion.

Never repeat sensitive material unnecessarily in a withdrawal notice.

## 15. Release sequence

Use this lifecycle:

`private embryo -> private incubation -> private clearance -> repository-safe public-source staging -> web QA -> author release -> live verification -> POSSE -> maintenance/correction`

No search, RSS, social, POSSE, or syndication step precedes canonical publication on `bhalaji.com`.

The private stages live outside this public repository. See `research-notes-lifecycle.md`.

## 16. Human review remains mandatory

Automation can detect missing metadata and known unsafe states; it cannot decide whether an idea is confidential, whether a sponsor/journal term applies, whether a figure exceeds a license, or whether a disclosure creates patent, ethics, privacy, export, or collaboration risk.

A passing CI check is necessary but not sufficient. When judgment is uncertain, keep the material in the private incubation environment and use the appropriate PI, collaborator, VCU ethics/compliance, technology-transfer, sponsor, journal, or other authoritative channel.