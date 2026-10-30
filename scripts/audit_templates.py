#!/usr/bin/env python3
"""Static checks for the custom Hugo layout system before rendering."""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = ROOT / "layouts"


def main() -> int:
    errors: list[str] = []
    templates = sorted(LAYOUTS.rglob("*.html"))
    if not templates:
        errors.append("no Hugo templates found")
    for path in templates:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if text.count("{{") != text.count("}}"):
            errors.append(f"{relative}: unbalanced Hugo template delimiters")
        # Only page templates are required to define the main block. Partials,
        # shortcodes, and Goldmark render hooks are invoked by other templates.
        if (
            "partials" not in path.parts
            and "shortcodes" not in path.parts
            and "_markup" not in path.parts
            and path.name != "baseof.html"
        ):
            if '{{ define "main" }}' not in text:
                errors.append(f"{relative}: missing main template definition")
        for image in re.findall(r"<img\b[^>]*>", text, flags=re.IGNORECASE):
            for attribute in ("src=", "alt=", "width=", "height="):
                if attribute not in image:
                    errors.append(f"{relative}: image missing {attribute[:-1]}: {image[:140]}")

    base = (LAYOUTS / "_default/baseof.html").read_text(encoding="utf-8")
    for marker in ('partial "seo_head.html"', 'partial "site_header.html"', 'block "main"', 'partial "site_footer.html"'):
        if marker not in base:
            errors.append(f"layouts/_default/baseof.html: missing {marker}")
    for marker in ('data-analytics-consent="unknown"', 'data-consent-bootstrap', 'bhalaji.analyticsConsent.v1', 'dataset.analyticsConsent'):
        if marker not in base:
            errors.append(f"layouts/_default/baseof.html: missing prepaint consent marker {marker}")
    for marker in ('resources.FromString "css/core.css"', 'resources.Concat "css/site.css"', 'fingerprint "sha384"'):
        if marker not in base:
            errors.append(f"layouts/_default/baseof.html: missing bundled CSS marker {marker}")

    seo_head = (LAYOUTS / "partials/seo_head.html").read_text(encoding="utf-8")
    mastodon_head_marker = '<link rel="me" href="https://infosec.exchange/@bhalaji">'
    if mastodon_head_marker not in seo_head:
        errors.append("SEO head must retain the Mastodon rel=me verification link")
    if '"https://infosec.exchange/@bhalaji"' not in seo_head:
        errors.append("Person structured data must retain Mastodon in sameAs")

    # Scholarly metadata must be scoped to the three canonical output records.
    landing = (LAYOUTS / "landing/list.html").read_text(encoding="utf-8")
    if '{{ if not .IsHome }}{{ partial "privacy_controls.html" . }}{{ end }}' not in base:
        errors.append("homepage privacy notice must no longer precede the introduction")
    if not (landing.find('class="hero"') < landing.find('partial "privacy_controls.html"') < landing.find('id="research"')):
        errors.append("homepage consent choices must follow the introduction before the Research section")

    if 'partial "home_proof.html"' in landing:
        errors.append("homepage should not contain the old numerical counter strip")
    if not all(marker in landing for marker in ('class="home-experience"', 'home-disclosure--experience', 'open data-responsive-experience', 'partial "home_experience_body.html"')):
        errors.append("Experience must use one progressive-enhancement disclosure")
    if landing.count('partial "home_experience_body.html"') != 1:
        errors.append("homepage Experience chronology must not be rendered twice")

    statement_path = ROOT / "content/research-statement/index.md"
    research_page = (ROOT / "content/research/index.md").read_text(encoding="utf-8")
    if not statement_path.exists():
        errors.append("standalone research statement missing")
    else:
        statement = statement_path.read_text(encoding="utf-8")
        for heading in ("## Research motivation", "## Foundation in experimental measurement", "## Doctoral research direction", "## Questions and boundaries"):
            if heading not in statement:
                errors.append(f"research statement missing grounded section {heading}")
    if "(/research-statement/)" not in research_page:
        errors.append("Research page must link to its research statement")

    scholar_records = {
        "adhesives-wearable": ('scholar_journal: "Polymers"', 'scholar_volume: "18"', 'scholar_issue: "12"'),
        "electrospun-fiber-mats": ("scholar_journal: 'Polymers'", "scholar_volume: '17'", "scholar_issue: '13'"),
        "masters-thesis": ('scholar_dissertation_institution: "Virginia Commonwealth University"', 'scholar_doi: "10.25772/f6wc-rh09"'),
    }
    for slug, markers in scholar_records.items():
        record = (ROOT / "content/publication" / slug / "index.md").read_text(encoding="utf-8")
        for marker in markers:
            if marker not in record:
                errors.append(f"authoritative Scholar metadata missing in {slug}: {marker}")
    for meta in ("citation_title", "citation_author", "citation_publication_date", "citation_journal_title", "citation_volume", "citation_issue", "citation_dissertation_institution", "citation_doi"):
        if f'name="{meta}"' not in seo_head:
            errors.append(f"publication head missing Scholar citation tag {meta}")
    if 'name="citation_pdf_url"' in seo_head:
        errors.append("do not advertise an unverified publication PDF as a hosted full-text asset")

    header = (LAYOUTS / "partials/site_header.html").read_text(encoding="utf-8")
    for marker in ('class="brand__monogram"', 'viewBox="0 0 40 40"', 'fill="currentColor"'):
        if marker not in header:
            errors.append(f"shared header must retain the canonical vector BK monogram marker {marker}")
    if "https://infosec.exchange/@bhalaji" in header:
        errors.append("shared header must not contain a redundant Mastodon verification backlink")

    # Primary navigation is intentionally canonical and stable across pages; do not
    # restore the old mix of homepage fragments and standalone destinations.
    canonical_url_markers = (
        '{{ $aboutURL := "about/" | relURL }}',
        '{{ $researchURL := "research/" | relURL }}',
        '{{ $outputsURL := "outputs/" | relURL }}',
        '{{ $experienceURL := "experience/" | relURL }}',
        '{{ $engagementURL := "engagement/" | relURL }}',
        '{{ $contactURL := "contact/" | relURL }}',
    )
    for marker in canonical_url_markers:
        if marker not in header:
            errors.append(f"shared header lost canonical primary destination marker {marker!r}")
    nav_markers = (
        '>About</a>',
        '>Research</a>',
        '>Outputs</a>',
        '>Experience</a>',
        '>Engagement</a>',
        '>Contact</a>',
    )
    nav_positions = [header.find(marker) for marker in nav_markers]
    if any(position < 0 for position in nav_positions):
        errors.append("shared header must retain About, Research, Outputs, Experience, Engagement, and Contact navigation")
    elif nav_positions != sorted(nav_positions):
        errors.append("shared header navigation must keep the primary information architecture in order")
    for obsolete in ('#research', '#outputs', '#experience', '#presentations', '#contact'):
        if obsolete in header:
            errors.append(f"shared header must not mix canonical navigation with homepage fragment {obsolete!r}")
    if 'href="{{ $root }}#trajectory"' in header:
        errors.append("shared header must keep doctoral trajectory within Research rather than primary navigation")
    if 'aria-current="page"' not in header:
        errors.append("shared header must expose current standalone pages to assistive technology")

    trajectory = (LAYOUTS / "partials/home_trajectory.html").read_text(encoding="utf-8")
    if ">Open research questions</h3>" not in trajectory:
        errors.append("doctoral collaboration block must use the reader-facing 'Open research questions' heading")
    if "Questions worth combining methods around" in trajectory:
        errors.append("doctoral collaboration block must not restore process-oriented collaboration wording")

    # Progressive disclosure must retain underlying doctoral and engagement records.
    home = (LAYOUTS / "landing/list.html").read_text(encoding="utf-8")
    for html, label in ((trajectory, "doctoral"), (home, "engagement")):
        if 'class="home-disclosure ' not in html or '<summary>Explore ' not in html:
            errors.append(f"homepage {label} disclosure must retain native details/summary markup")
        if 'class="home-disclosure__body"' not in html:
            errors.append(f"homepage {label} disclosure must retain its evidence body")
    if not all(marker in trajectory for marker in ('class="trajectory-grid"', 'class="questions__grid"', 'Open research questions')):
        errors.append("homepage doctoral section must preserve visible questions and disclosed supporting evidence")
    questions_pos = trajectory.find('<section class="questions"')
    details_pos = trajectory.find('<details class="home-disclosure')
    methods_pos = trajectory.find('class="trajectory-grid"')
    if min(questions_pos, details_pos, methods_pos) < 0 or not (questions_pos < details_pos < methods_pos):
        errors.append("doctoral questions must be visible before the closed methods/applications disclosure")
    if not all(link in trajectory for link in ('href="{{ "/research-statement/" | relURL }}"', 'Explore measurement methods and application directions')):
        errors.append("doctoral section must link to research statement while the disclosure labels only supplementary material")
    about_template = (LAYOUTS / "about/single.html").read_text(encoding="utf-8")
    if 'href="{{ "/research-statement/" | relURL }}"' not in about_template:
        errors.append("About must link to the research statement")
    if '{{ .text | markdownify }}' not in about_template:
        errors.append("About chronology must render canonical research evidence links as hyperlinks")
    cv_builder = (ROOT / "scripts/build_cv.py").read_text(encoding="utf-8")
    cv_data = (ROOT / "data/cv.yaml").read_text(encoding="utf-8")
    if 'href(p["research_statement"], "Research statement (online)")' not in cv_builder or 'research_statement: https://bhalaji.com/research-statement/' not in cv_data:
        errors.append("academic CV must link to the research statement from canonical data")
    research_short = (LAYOUTS / "partials/research_signature.html").read_text(encoding="utf-8")
    methods_short = (LAYOUTS / "shortcodes/method-schematic.html").read_text(encoding="utf-8")
    if '<ol class="research-signature__flow"' not in research_short or '<ol class="method-schematic__steps"' not in methods_short:
        errors.append("scientific diagrams must use accessible intrinsic-size text, not scaled SVG labels")
    if '<svg' in research_short or '<svg' in methods_short:
        errors.append("workflow diagrams must not shrink text inside SVG viewBox coordinates")
    if "Schematic; no quantitative data are implied." in research_short or "Schematic; no quantitative data are implied." in methods_short:
        errors.append("visitor-facing captions must not expose internal schematic disclaimers")
    for target in (
        'https://bhalaji.com/project/quantitative-thermal-imaging/',
        'https://bhalaji.com/project/peel-trace-evaluation/',
    ):
        if target not in cv_data:
            errors.append(f"CV/resume project-title destination missing: {target}")
    if 'title = href(item["details_url"], item["title"]) if item.get("details_url") else esc(item["title"])' not in cv_builder:
        errors.append("CV and resume project titles must link to their established evidence pages")
    if not all(marker in trajectory for marker in ('Controlled histories and repeatable measurement', 'Potential application directions')):
        errors.append("doctoral research evidence must distinguish measurement methods from potential applications")
    research_page = (ROOT / "content/research/index.md").read_text(encoding="utf-8")
    research_statement = (ROOT / "content/research-statement/index.md").read_text(encoding="utf-8")
    if "model system" not in research_page or "model system" not in research_statement:
        errors.append("research content must explain the cholesteric model-system role")
    if "infrared thermography" not in research_page.lower() or "computational infrared thermography" not in research_statement.lower():
        errors.append("research content must distinguish exploratory infrared software from thermochromic sensing")
    if "no physiological\ninference or diagnostic capability is claimed" not in research_page.lower():
        errors.append("Research applications must explicitly distinguish exploratory thermography from validated physiological inference")
    # Homepage selected-outputs heading must introduce the featured study without
    # becoming a four-line inventory of every possible output type.
    if "<h2>Published research and tools.</h2>" not in home:
        errors.append("homepage selected-outputs heading must remain concise")
    if "The first-author article, associated thesis, and citable software document the same study." not in home:
        errors.append("homepage selected-outputs introduction must explain the related work")

    if not all(marker in home for marker in ('class="series-grid"', 'class="engagement-grid"', 'View full professional engagement')):
        errors.append("homepage engagement disclosure must preserve records and the full-engagement link")

    footer = (LAYOUTS / "partials/site_footer.html").read_text(encoding="utf-8")
    if "https://infosec.exchange/@bhalaji" in footer:
        errors.append("shared footer must not expose Mastodon after verification is established")

    about_layout = (LAYOUTS / "about/single.html").read_text(encoding="utf-8")
    for marker in ('class="about-fact-strip"', 'class="about-section__intro"', 'class="about-path__marker"', 'Professional path in chronological order'):
        if marker not in about_layout:
            errors.append(f"About template lost structural marker {marker!r}")
    if 'about-portrait__caption' in about_layout:
        errors.append("About portrait must not repeat name, role, and location already present in the page hierarchy")
    if 'about-program-grid' in about_layout:
        errors.append("About must not duplicate the homepage research-program card grid")
    about_content = (ROOT / "content/about.md").read_text(encoding="utf-8")
    if "bio:\n  - >-" not in about_content:
        errors.append("content/about.md: biography entries must remain explicit YAML block scalars")

    for required in (
        LAYOUTS / "outputs/list.html",
        LAYOUTS / "experience/list.html",
        LAYOUTS / "engagement/list.html",
        LAYOUTS / "contact/list.html",
    ):
        if not required.exists():
            errors.append(f"{required.relative_to(ROOT)}: primary destination template missing")

    outputs_layout = LAYOUTS / "outputs/list.html"
    if outputs_layout.exists():
        outputs = outputs_layout.read_text(encoding="utf-8")
        for marker in ('Research software', 'Intellectual property record', 'Peer-reviewed article'):
            if marker not in outputs:
                errors.append(f"outputs hub lost record type {marker!r}")
        if 'role="group" aria-label="Filter research outputs by type"' not in outputs:
            errors.append("outputs filter must retain a concise accessible group label")
        if outputs.count('data-output-filter=') != 5:
            errors.append("outputs filter must retain exactly five type choices")
        if "output-filter__label" in outputs or re.search(r">\s*Show\s*<", outputs, flags=re.IGNORECASE):
            errors.append("outputs filter must not reintroduce a redundant visible Show label")
        # Identically titled article and thesis must retain formal titles, distinct accessible labels,
        # and bidirectional record links rather than inventing new publication names.
        for marker in (
            'aria-label="{{ $thesisPage.Title }} (M.S. thesis)"',
            'aria-label="{{ $primary.title }} (peer-reviewed journal article)"',
            'href="{{ $primaryPage.RelPermalink }}">Related journal article',
            'href="{{ $thesisPage.RelPermalink }}">Related M.S. thesis',
        ):
            if marker not in outputs:
                errors.append(f"outputs hub lost journal/thesis disambiguation: {marker!r}")

    privacy = (LAYOUTS / "partials/privacy_controls.html").read_text(encoding="utf-8")
    banner = re.search(r'<section\b[^>]*data-privacy-banner[^>]*>', privacy)
    if not banner:
        errors.append("privacy notice must retain the shared data-privacy-banner element")
    elif re.search(r'\bhidden\b', banner.group(0)):
        errors.append("privacy notice must render from the prepaint consent state, not reveal later from deferred JavaScript")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        f"Template audit passed: {len(templates)} Hugo templates checked, "
        "including shortcodes and render hooks without treating them as page templates."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
