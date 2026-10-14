# Research publishing and visibility strategy

This document governs **why** a Research Note should exist, how publication effort is allocated, and how useful public work compounds into credible discovery. It is distinct from `research-notes-governance.md`, which determines whether material may be disclosed, and from design governance, which determines how the public experience should behave.

The operating order is:

`governance -> evidence -> reader utility -> strategic fit -> publication quality -> discovery -> distribution -> measurement -> maintenance`

Traffic, posting frequency, and social reach never override research ethics, evidence quality, ownership, confidentiality, intellectual-property constraints, or scientific accuracy.

## 1. North star

The objective is **qualified discovery of verifiable research expertise**.

A successful visit is not merely a page view. The strongest outcome is that a reader who did not already know the author:

1. finds a useful technical explanation;
2. understands the scientific question or method more clearly;
3. can inspect the supporting evidence and provenance;
4. can move naturally to a publication, thesis, software release, presentation, or research program; and
5. leaves with an accurate understanding of the author's expertise and its limits.

## 2. Three independent decisions

Every prospective note answers three questions in order:

- **Can we publish it?** -> research governance and disclosure clearance.
- **Should we publish it?** -> strategic value, reader utility, evidence strength, and maintenance burden.
- **How should it appear?** -> editorial structure, visuals, accessibility, metadata, and performance.

A high strategic score cannot compensate for an unresolved governance gate.

## 3. Eligibility gate before prioritization

Do not score unsafe material. A candidate must first pass:

1. **Repository-safe** — nothing in the candidate is unpublished, confidential, collaborator-restricted, sponsor-restricted, embargoed, uncleared IP, regulated without clearance, or otherwise inappropriate for the public repository.
2. **Evidence-ready** — the key claims can be traced to verified public sources or cleared public work.
3. **Strategically relevant** — the note strengthens the site's coherent research identity rather than adding unrelated content volume.

If any answer is no or uncertain, hold the candidate outside the public repository.

## 4. Research-content portfolio model

Use a BCG-style portfolio model, adapted for scholarship rather than revenue.

### Stars

High evidence strength, high strategic importance, and growing relevance. Invest in excellent explanation, original schematics, companion notes, and strong links to public outputs.

### Cash cows / evergreen anchors

Mature, durable, well-supported subjects that repeatedly answer useful questions. Maintain citations, improve diagrams and internal links, and keep them current rather than replacing them with frequent new posts.

### Question marks

Promising subjects with uncertain reader demand, differentiation, or maintenance value. Test with a focused note before building a large content cluster.

### Merge, retire, or do not publish

Material with weak differentiation, low continuing utility, excessive maintenance cost, or overlap with a stronger page should be consolidated or omitted.

The labels are internal planning tools, not public-facing classifications.

## 5. Topic-priority model

After governance clearance, score candidate topics from 1–5 on:

- strategic alignment with the research identity — 25%;
- reader utility / job-to-be-done — 20%;
- evidence strength — 20%;
- evergreen value — 15%;
- discovery opportunity — 10%;
- reuse and linkability — 10%.

Then consider maintenance burden as a separate cost. Do not create a numerical disclosure-risk score; disclosure risk is a gate, not a tradeable variable.

For uncertain ideas, use a lightweight RICE/ICE test: likely reach, scientific/professional impact, confidence in the evidence, and effort to create and maintain the note.

## 6. Jobs-to-be-done

Every public page has one primary reader job. Examples:

- understand what a measurement actually means;
- decide which characterization approach fits a scientific question;
- understand why a processing variable changes interpretation;
- inspect how an analysis workflow becomes reproducible;
- obtain enough context to understand a publication or software record;
- evaluate whether the researcher's expertise is relevant to a problem.

If the primary reader job cannot be stated clearly, reconsider the page.

## 7. Rhetorical models by content type

Use the structure that fits the evidence rather than forcing every page into one template.

### Research Note

`question -> evidence -> reasoning -> implications -> limitations`

### Methods Note

`problem -> measurement -> method -> failure modes -> interpretation -> limitations`

### Research reflection

`context -> assumption -> observation -> revision -> current view`

### Professional/project case study

Use **STAR + Evidence + Limits**:

`situation -> task -> action -> result -> evidence -> limitations`

STAR is useful for professional narratives but must not be used to imply causal certainty that the evidence does not support.

## 8. Evidence ladder

Writing should reveal the epistemic status of important claims.

1. hypothesis / open question;
2. methodological perspective or practice preference;
3. evidence-supported interpretation;
4. publicly documented own result;
5. established or peer-reviewed evidence.

Language should become stronger only as evidentiary support becomes stronger. A note should distinguish observation, inference, hypothesis, interpretation, and established literature rather than flatten them into the same voice.

## 9. Knowledge graph and topic clusters

The Notes section is a knowledge graph, not a chronological feed.

Build clusters around genuine research programs and methods. A note should link to the closest relevant:

- research-program page;
- publication or thesis;
- research software;
- presentation or public output;
- related note.

Use descriptive anchor text that states the relationship. Internal links should help both readers and search systems understand the context of a page.

Do not create topic/tag pages until there is enough material to make them useful.

## 10. Evergreen/timely barbell

Default toward approximately 75–85% evergreen material: methods, concepts, measurement problems, interpretation, and reproducibility.

Use the remaining share for timely but already-public developments such as a newly public paper, software release, conference synthesis, or cleared methodological development.

Do not chase general trends merely to increase publishing frequency.

## 11. Credibility moat

The site's advantage should be evidence density rather than article count.

A strong note may connect:

`note -> primary literature -> own public research -> software/data -> thesis/paper -> related methods -> research program`

Prefer five highly inspectable notes with durable evidence over fifty generic articles.

## 12. Visual decision model

A visual must reduce cognitive load or communicate a relationship more effectively than prose.

- what is happening? -> conceptual schematic;
- in what order? -> process diagram;
- how are concepts connected? -> relationship map;
- how does a quantity change? -> plot;
- where is the important region? -> annotated trace;
- how does an experiment work? -> geometry/setup schematic;
- which option fits? -> decision matrix;
- what are the trade-offs? -> comparison table.

No decorative image quota is used. Scientific visuals follow `docs/design-governance.md` and the publication-governance provenance rules.

## 13. Progressive disclosure for readers

A note should work at three reading depths:

- **5 seconds:** title and one-sentence proposition;
- **30 seconds:** standfirst / in-brief summary, descriptive headings, and a useful figure when appropriate;
- **5–10 minutes:** full reasoning, limitations, evidence, and references.

Technical depth is preserved; it is organized rather than removed.

## 14. Discovery without search-engine-first writing

Write for the scientific question while making terminology explicit enough that readers using adjacent vocabulary can still find the page.

Bridge specialist and conceptual terms naturally, for example:

`thermomechanical history <-> processing history <-> prior temperature and deformation`

Avoid keyword repetition, manufactured search pages, generic definitions with no original value, or content created primarily to capture traffic.

Useful discovery infrastructure includes semantic HTML, canonical URLs, structured data, accurate metadata, descriptive internal links, accessible figures, stable URLs, sitemaps, and genuinely helpful content.

Google's current Search guidance emphasizes people-first content, original analysis, demonstrable expertise, useful internal links, and clear authorship rather than publishing volume for search traffic:

- <https://developers.google.com/search/docs/fundamentals/creating-helpful-content>
- <https://developers.google.com/search/docs/fundamentals/seo-starter-guide>
- <https://developers.google.com/search/docs/appearance/structured-data/article>

## 15. Publish-own-site-first distribution

The canonical asset is the page on `bhalaji.com`.

Use POSSE: **Publish on Own Site, Syndicate Elsewhere**. Only after the canonical page is live may a concise derivative be shared to an appropriate professional network or linked from software/documentation.

Third-party distribution should point readers back to the canonical research note rather than create multiple competing versions.

## 16. Research visibility flywheel

`public research -> useful note -> qualified discovery -> evidence inspection -> paper/software/research exploration -> citation/share/conversation -> new questions -> stronger notes`

The purpose of publishing is not to finish a content task; it is to create a durable, inspectable interface between research and readers.

## 17. Measurement model

Do not optimize around page views alone. Review four dimensions:

### Discoverability

- indexed pages;
- impressions and qualified clicks;
- non-branded queries;
- relevant query diversity.

### Authority

- credible inbound links or references;
- movement from Notes to publications/software;
- institutional or scholarly referrals when observable.

### Reader utility

- which pages sustain useful engagement;
- which paths connect Notes to Research and Outputs;
- evidence-link use.

### Quality

- Core Web Vitals and Lighthouse trends;
- accessibility;
- broken links;
- stale or corrected references;
- maintenance burden and correction frequency.

Use Search Console periodically rather than reactively. Measurement informs maintenance and topic selection; it does not rewrite scientific claims.

## 18. Maintenance, correction, and retirement

Use a lifecycle rather than assuming pages are permanent and unchanged.

- minor typographic/link fixes may be corrected without a substantive revision marker;
- substantive scientific clarification updates `lastmod` and receives a short revision note;
- a material factual error receives a visible correction;
- a page that is no longer reliable receives a withdrawal/retirement notice rather than silent historical erasure;
- overlapping or low-value material may be merged into a stronger canonical page with an appropriate redirect.

A previously public page cannot be made historically private by deleting it. Treat public publication as effectively irreversible disclosure.

## 19. Adversarial review

Before release, red-team the note:

- Which statement is easiest to attack?
- Does every important citation support exactly what the prose claims?
- What could a collaborator, reviewer, sponsor, or technology-transfer office object to?
- Which sentence could be mistaken for a clinical, causal, or performance claim?
- Could a schematic be mistaken for empirical data?
- What would become false if a key assumption changed?
- Could a search snippet remove necessary uncertainty or context?

The goal is not defensive prose; it is calibrated claims.

## 20. Trust heuristic

Use this non-numerical decision heuristic:

`trust ~ (evidence × provenance × clarity × consistency) / (overclaim + ambiguity + staleness + unmanaged conflict)`

Increasing discoverability while increasing the denominator is a loss.

## 21. Review cadence

- review a note when a related publication, correction, software release, standard, or major source changes;
- perform a periodic source/link/status sweep through the repository integrity workflow;
- use observed search behavior to improve strong existing pages before defaulting to new content creation;
- revisit the portfolio classification at least annually or when the research program changes materially.

This strategy is intentionally conservative about volume. The goal is a small, compounding body of accurate, useful and interconnected scholarly explanations.