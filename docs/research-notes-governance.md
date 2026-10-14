# Research Notes publication governance

This document is the release standard for any public note published from this repository. It is deliberately conservative: a personal research website is a public disclosure channel, not a substitute for a laboratory, sponsor, journal, university, ethics, or technology-transfer review process.

The default rule is **fail closed**. If disclosure status, ownership, confidentiality, attribution, intellectual-property status, ethics, or conflict-of-interest treatment is uncertain, keep the note as a draft and obtain the appropriate clarification before publication.

## 1. Scope and authority

These rules apply to every file under `content/notes/` other than section index pages. They govern whether a note may be made public; they do not determine legal rights or replace institutional review.

The standard is grounded in current authoritative guidance, including:

- [VCU Research and Innovation — policies, procedures and compliance notices](https://research.vcu.edu/integrity-and-compliance/compliance/policies-procedures-and-compliance-notices/), which currently lists policies covering conflicts of interest in research, intellectual property, export compliance and research security, research data ownership/retention/access/security, research misconduct, human research protections, animal research, and sponsored-program obligations.
- [VCU conflicts of interest in research](https://research.vcu.edu/integrity-and-compliance/integrity-and-ethics/conflicts-of-interest-in-research/), which treats financial and other personal interests as matters requiring disclosure, assessment, and management to protect objectivity and research integrity.
- [VCU research ethics consultation](https://research.vcu.edu/integrity-and-compliance/research-ethics-consultation/), which explicitly covers authorship/publication questions, conflicts of interest, protocol issues, and research-integrity concerns.
- [HHS Office of Research Integrity RCR Casebook](https://ori.hhs.gov/rcr-casebook-introduction), which treats authorship/publication, collaboration, data management, conflicts of interest, mentor/trainee responsibilities, and social responsibility as overlapping responsible-conduct issues.
- [WIPO patent FAQ](https://www.wipo.int/en/web/patents/faq_patents) and [WIPO patent-protection guidance](https://www.wipo.int/en/web/patents/protection), which caution that public disclosure before filing can become prior art and can destroy novelty in many jurisdictions.
- [USPTO international patent guidance](https://www.uspto.gov/patents/basics/international-protection/filing-patents-abroad), which notes that the United States has a one-year inventor-originated disclosure grace period while many other jurisdictions may not protect patentability after pre-filing public disclosure.

When a VCU policy, sponsor agreement, journal policy, collaboration agreement, law, regulation, or formal instruction is more restrictive than this repository standard, the more restrictive requirement controls.

## 2. Permitted publication bases

A public Research Note must rest on at least one defensible public-disclosure basis:

1. `public_literature` — established public sources such as peer-reviewed literature, standards, authoritative technical guidance, or public datasets;
2. `published_own_work` — the author's already-public paper, thesis, dataset, software release, patent publication, or other stable scholarly record; or
3. `authorized_public_disclosure` — material already made public through an authorized channel, such as an approved public presentation or other cleared disclosure.

A note may combine these bases, but the front matter records the primary basis.

A manuscript being drafted, under review, accepted but embargoed, discussed internally, shown in a closed meeting, stored in a private repository, or included in a non-public patent application is **not** public merely because a future public release is expected.

## 3. Absolute hold conditions

A note remains `draft: true` if it contains or materially reveals any of the following unless the relevant material has already become an authorized public disclosure and any additional required approval has been obtained:

- unpublished experimental results, trends, images, datasets, formulations, parameters, or mechanistic conclusions;
- unpublished work of a collaborator, laboratory member, student, mentor, or external partner;
- confidential, NDA-bound, sponsor-restricted, export-controlled, security-sensitive, or otherwise restricted information;
- enabling details of potentially patentable subject matter that have not been cleared for public disclosure;
- peer-review material, grant-review material, internal research discussions, or non-public sponsor communications;
- identifiable or restricted human-subject information, non-public animal-research information, or material whose disclosure conflicts with an approved protocol or data-use condition;
- third-party figures, tables, photographs, text, or other copyrighted material without an applicable license, permission, or defensible original replacement.

Absence of numerical data is not sufficient to make a disclosure safe. A workflow, schematic, choice of variables, sequence of operations, interpretation, or framing can itself reveal unpublished intellectual contribution.

## 4. PI, collaborator, sponsor, and ownership rule

If another researcher could reasonably say, “this is partly our unpublished work,” the note is held until the appropriate author/PI/collaborator review is resolved.

If work was performed using university resources, within a laboratory, under sponsored research, under a collaboration, or in connection with institutional intellectual property, ownership and disclosure obligations must be checked before publication. A personal website does not supersede those obligations.

`ownership_review: complete` means the author has checked that the proposed public note does not conflict with applicable ownership, collaboration, sponsor, or laboratory obligations. It does not assert that the author personally owns every underlying research asset.

## 5. Intellectual-property rule

Treat a Research Note as a public disclosure.

If a note is potentially patent-sensitive, set `potentially_patent_sensitive: true`. The note cannot be published unless `ip_clearance: cleared` and the text stays within the authorized public scope.

A filed patent application does not automatically authorize disclosure of every implementation detail. A published patent application makes its published contents public, but related undisclosed improvements, data, know-how, or later inventions may remain sensitive.

If there is any uncertainty, consult the relevant institutional technology-transfer or intellectual-property contact before publication.

## 6. Research ethics and regulated research

For material involving human participants, animals, regulated data, export controls, dual-use concerns, controlled technology, or another formal oversight regime, publication requires compatibility with the applicable protocol, authorization, data-use terms, and institutional requirements.

Set `regulated_research_material: true` whenever a note touches such material. Publication then requires `ethics_review: cleared`.

For ordinary materials-science notes that do not involve regulated research, use `regulated_research_material: false` and `ethics_review: not_applicable`.

## 7. Conflicts of interest

Every public note receives a COI review.

Use one of:

- `coi_status: none_declared` — no relevant conflict identified for the note;
- `coi_status: disclosed` — a relevant relationship exists and is transparently disclosed in `coi_statement`;
- `coi_status: managed` — a relevant relationship is subject to a formal management arrangement and the public statement is appropriate to the allowed disclosure.

Potentially relevant interests can include financial interests, consulting/advisory relationships, employment, sponsorship, licensing interests, inventorship/patent interests, or other relationships that a reasonable reader could consider relevant to interpretation of the note.

The repository check enforces disclosure metadata; it does not determine whether an institutional COI filing or management plan is required.

## 8. Citation and evidentiary rule

A public note must contain a non-empty `sources` list and should distinguish:

- established scientific claims — supported by primary literature, standards, or authoritative sources where practicable;
- the author's published results — linked to the corresponding paper, thesis, dataset, software release, patent publication, or other public record;
- interpretation — written as interpretation rather than established fact and grounded in cited evidence;
- reflection or methodological preference — clearly framed as perspective rather than universal scientific fact.

Citations must be verified against the underlying source. AI output, search snippets, or a secondary summary are not substitutes for checking the cited record.

Raw AI/chat transcripts are not publication-ready source material. AI may assist drafting or adversarial review, but the final note must be independently checked for scientific accuracy, citations, disclosure safety, authorship, and provenance.

## 9. Copyright and figure provenance

Every published note requires `copyright_review: complete`.

Public figures are classified as one of:

- original schematic;
- original data already cleared for public use;
- public/openly licensed data or figure used within its license;
- adapted figure with appropriate rights and attribution;
- reproduced figure with permission;
- clearly labelled illustrative/simulated material;
- photograph with appropriate rights and disclosure clearance.

Illustrative or simulated material must never be presented in a way that could reasonably be mistaken for observed experimental evidence.

## 10. Required release metadata

Each note uses the `archetypes/notes.md` governance block. Drafts may retain pending review values. A note with `draft: false` must satisfy all automated checks in `scripts/check_notes_governance.py`.

At minimum a published note requires:

- a valid note type and status;
- a clear disclosure basis;
- no unpublished/collaborator/confidential material flags;
- IP clearance when patent-sensitive;
- ethics clearance when regulated-research material is involved;
- completed ownership and copyright review;
- completed COI review and statement when needed;
- explicit publication approval;
- at least one verified source.

## 11. Release sequence

Use this order for every Research Note:

`draft -> source/citation review -> disclosure review -> ownership/collaboration review -> IP review if applicable -> ethics/COI review -> copyright/figure review -> web/accessibility/performance checks -> publication approval -> merge -> live verification`

No search, social, RSS, POSSE, or syndication step is allowed to precede canonical publication on `bhalaji.com`.

## 12. Human review remains mandatory

Automation can detect missing metadata and known unsafe states; it cannot decide whether a scientific idea is confidential, whether a figure exceeds a license, whether a sponsor term applies, or whether a disclosure creates patent risk.

Accordingly, a passing CI check is necessary but not sufficient. When the scientific or governance judgment is uncertain, keep the note private and use the appropriate PI, collaborator, VCU ethics/compliance, technology-transfer, sponsor, or journal channel for clarification.