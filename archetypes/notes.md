---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
lastmod: {{ .Date }}
draft: true
summary: ""
note_type: concept # method | concept | reflection
status: evolving # stable | evolving
tags: []

# Research-governance metadata is deliberately fail-closed. Keep draft: true
# until every applicable review is resolved. See docs/research-notes-governance.md.
governance:
  disclosure_basis: "" # public_literature | published_own_work | authorized_public_disclosure
  contains_unpublished_research: true
  contains_unpublished_collaborator_material: true
  contains_confidential_or_sponsor_material: true
  potentially_patent_sensitive: true
  ip_clearance: "" # not_applicable | cleared
  regulated_research_material: false
  ethics_review: "" # not_applicable | cleared
  ownership_review: pending # pending | complete
  coi_status: "" # none_declared | disclosed | managed
  coi_statement: ""
  copyright_review: pending # pending | complete
  publication_approval: pending # pending | approved

# Every published note needs at least one independently verified source.
sources: []
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

Write the canonical note here. Keep it private/draft until the scientific,
citation, disclosure, ownership, IP, ethics/COI, copyright, and web-quality
gates in `docs/research-notes-governance.md` have been satisfied.
