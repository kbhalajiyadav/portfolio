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
