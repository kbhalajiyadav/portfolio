# Research Notes review gates

This document separates four decisions that must not be collapsed into a single `approved` state.

## 1. Repository safety

`repository_safe: true` means the candidate and its assets are defensible for public disclosure at the source level. It addresses disclosure basis, unpublished/collaborator material, confidentiality, IP, venue/embargo, ethics, export/dual-use, ownership, privacy, funding, external-tool input, copyright, and related repository-boundary questions.

It does **not** by itself authorize the irreversible act of pushing the source to a public repository.

## 2. Intentional public-Git staging

`repository_staging_decision: approved` records the author's explicit decision to cross the public-source disclosure boundary.

This is separate from `repository_safe` because:

- something can be safe to disclose without the author wanting to disclose it yet;
- `draft: true` does not make public Git private;
- staging may be useful for PR/CI review while website publication remains blocked.

A note cannot enter public Git while this decision is `pending`.

## 3. Editorial value / non-redundancy

`editorial_value_review: complete` means the note has a distinct reader job and durable explanatory value. It should not exist merely to repeat an abstract, README, CV entry, or search keyword.

The review asks:

- What does this note help a reader understand or do that the primary publication/software page does not already provide?
- Is the note synthesis, explanation, method interpretation, or reflection rather than repackaging?
- Does it avoid substantial unnecessary textual overlap with the author's prior publication?
- Would the note still deserve to exist if search traffic were ignored?

This is a strategic/editorial gate, not a claim of scientific novelty.

## 4. Independent human scientific review

Use:

- `external_scientific_review_required: true|false`
- `external_scientific_review_status: pending|complete|not_required`

A repository-safe draft may use `required: true` with `status: pending` while it remains `draft: true`.

When independent review is required, the note cannot publish with `draft: false` until `external_scientific_review_status: complete`.

Independent human review is especially appropriate when a note:

- interprets collaborative/co-authored research;
- explains method terminology that could be overread mechanistically;
- synthesizes a result beyond the wording of the primary paper;
- may affect how another researcher applies a method;
- touches a domain where an expert could identify a missing caveat that automated review cannot.

A suitable reviewer may be a co-author/PI or another knowledgeable researcher. This field does not imply institutional approval or formal peer review unless that actually occurred.

### Privacy rule for reviewer feedback

The public repository should store only the minimum non-sensitive outcome needed for release governance. Do **not** paste unpublished results, private lab discussion, confidential reviewer correspondence, sponsor-restricted information, or other non-public context into a public issue or commit merely to prove that a review occurred.

Substantive discussion may happen through an appropriate private/approved channel. After review, the public metadata can record only `complete` plus a non-sensitive revision summary if needed.

## 5. Live author release

`author_release_decision: approved` is the author's final decision to make the canonical note live on `bhalaji.com`.

It is distinct from:

- repository safety;
- public-Git staging consent;
- independent scientific review;
- institutional/PI/sponsor/journal/legal approval.

For a note requiring independent scientific review, the safe sequence is:

`repository safe -> author approves public-Git staging -> draft source / CI -> independent human scientific review -> re-audit substantive changes -> author approves live release -> draft:false -> live verification`

No automatic promotion is permitted between these states.
