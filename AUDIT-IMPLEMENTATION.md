# Portfolio audit and implementation record

Reviewed and consolidated on July 28, 2026.

## Implemented

- Reduced the homepage to seven functional sections: hero/status, research, outputs, experience/education, presentations/teaching/service, doctoral trajectory, and contact.
- Removed the reading-progress bar and both duplicate JavaScript implementations.
- Replaced two visual systems with one header, footer, token set, responsive grid system, hover/focus policy, and article layout.
- Replaced the stale incoming-doctoral language with current Ph.D. student positioning.
- Grouped the first-author article, M.S. thesis, and research software as one connected research package.
- Corrected ambiguous labels: Article, Article PDF, Thesis record, Source code, Software release, and All versions.
- Removed the wrong “See the evidence workflow” destination and created a stable `/research/` page.
- Kept robotics as repeatability infrastructure rather than a separate research identity.
- Excluded unsupported infrared and defense-specific claims.
- Added explicit application boundaries so future directions are not presented as demonstrated devices.
- Removed repeated internal author cards and redundant dividers.
- Moved page topics into the header and implemented a 320 px table of contents that collapses naturally on smaller screens.
- Added intermediate breakpoints for laptops and small desktops.
- Added reduced-motion handling and visible keyboard focus.

## Search and AI retrieval

- Added canonical metadata, social preview metadata, a dedicated OG card, and consistent descriptions.
- Added a `ProfilePage`/`Person` identity graph with ORCID, Scholar, GitHub, and LinkedIn `sameAs` records.
- Added `rel="me"` links in the document head and profile links.
- Added explicit crawler rules that permit conventional indexing and OpenAI/Anthropic search retrieval while blocking their separate model-development crawlers; also added the sitemap declaration, `llms.txt`, `llms-full.txt`, and IndexNow notification.
- Added placeholders for Google Search Console and Bing Webmaster Tools verification codes; no values were invented.

## Validation gates

- `scripts/audit_source.py` prevents known regressions, including stale status, duplicate progress code, sample URLs, misdirected workflow links, and ambiguous labels.
- `scripts/check_site.py` checks generated HTML metadata, duplicate IDs, local resources, and fragment targets.
- The CV is regenerated from YAML and compiled during deployment.
- IndexNow runs only after deployment and cannot fail the deployment.

## Manual ownership steps after deployment

1. Add and verify `https://bhalaji.com/` in Google Search Console.
2. Add and verify the domain in Bing Webmaster Tools.
3. Paste the issued verification codes into `config/_default/params.yaml` and redeploy.
4. Submit or inspect `https://bhalaji.com/sitemap.xml` in both services.
5. Request indexing for the homepage and `/research/` after the first deployment.

These service-side steps cannot be completed from repository code alone because they require account-level domain ownership confirmation.

## IndieWeb and branch-feature review addendum

The `agent/academic-portfolio-redesign` branch was reviewed as a feature source, not as
a replacement design. The final build keeps the current palette, scientific motifs,
portrait treatment, seven-section information architecture, and grouped disclosure
components.

Adopted:

- the compact square `BK` monogram, rebuilt inside the shared header;
- the existing accessible mobile menu, active-section state, native `<details>`
  disclosures, and copy-citation behavior;
- representative h-card, h-entry, feed discovery, and conditional IndieWeb endpoint
  discovery;
- a dormant notes/POSSE template that adds no homepage weight.

Rejected:

- a desktop navigation dropdown, because the current navigation remains shallow;
- the standalone animated metrology showcase, 3-D pointer tilt, and scanning animation;
- a separate latest-updates section and flat presentation archive;
- automatic syndication before real target accounts and endpoint credentials are set.

The result adds identity and owned-publishing infrastructure without changing the
portfolio's current visual hierarchy or adding public content.
## GitHub Actions Node.js 24 compatibility

The deployment workflows now use Node.js 24-compatible action releases:

- `actions/checkout@v6` in both workflows;
- `actions/configure-pages@v6`;
- `actions/upload-pages-artifact@v5`; and
- `actions/deploy-pages@v5`.

The Hugo workflow also checks out the repository before installation and build steps.
This removes the deprecated Node.js 20 action annotations while preserving the
existing build, generated-site audit, Pages deployment, and IndexNow notification.


## Production-hardening correction

- Removed the unused legacy `content/authors/` profile archive that generated `/authors/page/1/` through a HugoBlox-specific template without the unified metadata head.
- Reduced public taxonomies to `tags` only; author, category, and publication-type values remain content metadata but no longer generate duplicate archive pages.
- Added explicit terms and taxonomy templates using the shared header, footer, metadata, and interaction system.
- Added descriptive section records for publications, projects, and research topics.
- Made `ProfilePage.dateModified` data-driven rather than hard-coded.
- Added source and generated-site regression gates that fail if a legacy authors archive returns.
- Added workflow timeouts and generated-site diagnostics; removed the unused Node dependency-install step.
