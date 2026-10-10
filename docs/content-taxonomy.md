# Portfolio content taxonomy

This file records where portfolio facts live and how public pages relate to one another. It prevents duplicated facts and ambiguous navigation.

## Canonical structured sources

- `data/portfolio.yaml` — public profile, research-program language, presentations, experience, education, teaching, service, collaboration questions, and homepage/editorial records.
- `data/cv.yaml` — canonical CV facts and the source for the generated CV.
- `data/current_affiliation.yaml` — current lab/advisor/institutional-link context.
- `data/site_controls.yaml` — presentation limits and feature controls.
- publication/project front matter — record-specific metadata that belongs to that public record.

When the same factual claim appears in more than one surface, automated consistency checks should compare it with its canonical source rather than relying on manual synchronization.

## Public information levels

### Primary destinations

These are first-level destinations represented in persistent navigation:

- `/about/` — identity, biography, research identity, professional path, methods, profiles;
- `/research/` — scientific questions, measurement logic, doctoral direction, connected work;
- `/outputs/` — publications, thesis, citable software, intellectual property;
- `/experience/` — professional/research experience, education, research training;
- `/engagement/` — presentations, teaching/guidance, service, applied innovation;
- `/contact/` — collaboration and contact routes.

Primary destinations orient through the persistent header and therefore do not use a redundant back-to-home control.

### Detail records

Detail records sit one level below a primary destination and should expose a contextual parent link:

- `/publication/...` -> `/outputs/`;
- research-software records -> `/outputs/`;
- intellectual-property records -> `/outputs/`;
- research projects -> `/research/`;
- industry case studies -> `/experience/`;
- research notes -> `/notes/` when notes are public.

### Utility pages

Privacy, rights/brand-use, 404, machine-readable resources, and similar utility pages are not primary portfolio destinations. Their navigation can use a home route or other utility-appropriate recovery pattern.

## Homepage role

The homepage is the argument for the portfolio, not a complete duplicate of every destination page. It should establish research identity, major evidence, selected experience/engagement, and clear routes to the canonical destination pages.

## Evidence links

Link text that names a specific artifact or presentation series should resolve to the artifact/series itself. Generic section anchors are insufficient when the link text is more specific than the destination.

See `docs/design-governance.md` for the sitewide design and evidence-link rules.
