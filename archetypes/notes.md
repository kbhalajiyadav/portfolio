---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
lastmod: {{ .Date }}
draft: true
summary: ""
in_brief: "" # concise 2–3 sentence synthesis for the 30-second reading layer
note_type: concept # method | concept | reflection
status: evolving # stable | evolving | corrected | retired | withdrawn
featured: false
toc: false
social_card: research
tags: []
image: ""
image_alt: ""

# Lifecycle/display metadata. Required conditionally by the publication guard.
revision_note: "" # required when status=corrected
status_reason: "" # required when status=retired or withdrawn
replacement_url: "" # optional for retired/withdrawn notes
funding_statement: "" # public statement only when relevant
acknowledgements: "" # public acknowledgement only with appropriate consent
revisions: [] # substantive public revisions only; entries: {date: YYYY-MM-DD, summary: "..."}

# IMPORTANT: this repository is public. `draft: true` only prevents Hugo from
# rendering the page; it does NOT make this source private. Do not commit this
# file until repository_safe=true and every repository-boundary review below
# is resolved. Drafting before that belongs in the private incubation workspace.
governance:
  repository_safe: false
  disclosure_basis: "" # public_literature | published_own_work | authorized_public_disclosure
  contains_unpublished_research: true
  contains_unpublished_collaborator_material: true
  contains_confidential_or_sponsor_material: true

  potentially_patent_sensitive: true
  ip_clearance: "" # not_applicable | cleared

  venue_policy_review: "" # not_applicable | cleared
  embargo_status: "" # none only for material entering this public repository

  regulated_research_material: false
  ethics_review: "" # not_applicable | cleared
  export_control_review: "" # not_applicable | cleared
  dual_use_review: "" # not_applicable | cleared

  ownership_review: pending # pending | complete
  contributor_review: pending # pending | complete
  funding_review: pending # pending | complete
  privacy_review: pending # pending | complete
  external_tool_review: pending # pending | complete

  coi_status: "" # none_declared | disclosed | managed
  coi_statement: ""
  copyright_review: pending # pending | complete
  source_status_review: pending # pending | complete

  # This is the author's release decision, not a representation of institutional approval.
  author_release_decision: pending # pending | approved

# Published notes need independently verified sources. Public-source staging may
# still refine this list, but factual claims must be fully verified before release.
sources: []

# Use site-relative content paths so Hugo can verify these relationships.
# Examples: /publication/example/, /project/example/, /notes/example/
related_publications: []
related_software: []
related_projects: []
related_notes: []

# Add public copies only after canonical publication and successful syndication.
# syndication:
#   - name: LinkedIn
#     url: https://www.linkedin.com/posts/...
#   - name: Bluesky
#     url: https://bsky.app/profile/.../post/...
---

This file is **public-source staging**, not a private draft environment.

Develop rough or unpublished material in the private incubation workspace described
in `docs/research-notes-lifecycle.md`. Copy a candidate here only after it is safe
to disclose publicly. Keep `draft: true` while editorial, design, accessibility,
metadata, performance, and final publication checks are still in progress.
